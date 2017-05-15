from multimedia.constants import AUDIO_OUTPUT_ANALOG, AUDIO_OUTPUT_DIGITAL

def to_audio_output_multimedia(json_object):

    audio_output = AUDIO_OUTPUT_DIGITAL
    if 'audioout' in json_object:
        if json_object['audioout'] == 'analog':
            audio_output = AUDIO_OUTPUT_ANALOG

    return audio_output

def to_audio_output_string(audio_output):

    if audio_output == AUDIO_OUTPUT_ANALOG:
        return 'analog'

    return 'digital'
