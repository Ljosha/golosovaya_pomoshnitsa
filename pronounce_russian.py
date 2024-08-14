from functions import *

def main():

    while True:
        record_audio_until_silence(filename="output.wav", silence_threshold=0.01, silence_duration=2)
        text = extract_russian_text()
        print(text)

        pon = 'net'

        if 'привет' in text:
            proiznosheniye('Привет, как дела?')
            pon = 'da'

        if 'ты говоришь по-английски' in text:
            proiznosheniye("Я тупенькая немного и не разговариваю по-английски")

        if 'у меня все хорошо' in text:
            pon = 'da'
            proiznosheniye('Я очень рада что у вас всё хорошо')

        if text.startswith('напиши текст'):
            filename = 'tekst.txt'
            pon = 'da'
            with open(filename, 'w') as file:
                written_text = text[12:]
                file.write(written_text)
            proiznosheniye('Я написала следующее в отдельный текстовый файл' + written_text)

        if text == 'все':
            break

        if text.startswith('напиши папе'):
            soobshenie = text[12:]
            papa = ''
            send_whatsapp_message(papa, soobshenie)
            pon = 'da'

        if text.startswith('посмотри'):
            prompt = text[8:]
            response = lookup(prompt)
            proiznosheniye(response)
            pon = 'da'
            break

        if pon == 'net':
            proiznosheniye('Я не поняла')

if __name__ == "__main__":
        main()
