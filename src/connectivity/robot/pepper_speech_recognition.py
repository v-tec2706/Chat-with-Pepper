import argparse
import io
import re
import sys
import time

import numpy as np
import qi
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from naoqi import ALProxy
from six.moves import queue

from configuration import Configuration as configuration
from src.connectivity.socket.socket_conn_robot import DataExchangeModule

RATE = 16000


class SoundProcessingModule(object):
    """
    A simple get signal from the front microphone of Nao & calculate its rms power.
    It requires numpy.
    """

    def __init__(self, session):
        """
        Initialise services and variables.
        """
        super(SoundProcessingModule, self).__init__()
        self.audio_service = session.service("ALAudioDevice")
        session.registerService("SoundProcessingModule", self)
        self.isProcessingDone = True
        self.nbOfFramesToProcess = 20
        self.framesCount = 0
        self.closed = True
        self.micFront = []
        self.module_name = "SoundProcessingModule"
        self._buff = queue.Queue()
        self.file = io.open("rec", 'wb')
        self.tts = ALProxy("ALTextToSpeech", configuration.ROBOT_ADDRESS.value, configuration.ROBOT_PORT.value)
        self.tts.setLanguage("Polish")
        self.data_exchange_module = DataExchangeModule(configuration.ROBOT_ADDRESS.value,
                                                       configuration.ROBOT_SOCKET_PORT.value, self.tts)

    def __enter__(self):
        self.closed = False
        self.audio_service.setClientPreferences(self.module_name, RATE, 3, 0)
        self.audio_service.subscribe(self.module_name)
        self.isProcessingDone = False
        return self

    def __exit__(self, type, value, traceback):
        self.audio_service.unsubscribe(self.module_name)
        self.isProcessingDone = True
        self.closed = True
        self._buff.put(None)

    def startProcessing(self):
        """
        Start processing
        """
        self.audio_service.setClientPreferences(self.module_name, RATE, 3, 0)
        self.audio_service.subscribe(self.module_name)
        self.isProcessingDone = False

        while not self.isProcessingDone:
            time.sleep(0.5)

        self.audio_service.unsubscribe(self.module_name)

    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        self._buff.put(inputBuffer)

    def generator(self):
        while not self.isProcessingDone:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return

            data = np.frombuffer(chunk, np.int16)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data = np.concatenate((data, np.frombuffer(chunk, np.int16)), axis=None)
                except queue.Empty:
                    break

            yield data


def listen_print_loop(responses, mod):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            mod.data_exchange_module.send_data_and_tell_response(transcript + overwrite_chars)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                mod.isProcessingDone = True
                mod.closed = True
                break
            num_chars_printed = 0


def main(app):
    language_code = 'pl-PL'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with SoundProcessingModule(app) as stream:
        while not stream.closed:
            audio_generator = stream.generator()

            requests = (types.StreamingRecognizeRequest(audio_content=content.tobytes())
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            listen_print_loop(responses, stream)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.102",
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.1.102'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        # Initialize qi framework.
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
                                                                                              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
