# Chatbot com Rasa

Este bot retorna a temperatura. Exemplos de perguntas:
- me fale a temperatura de agora no Santa Catarina
- o dia está ensolarado no Rio de Janeiro?
- vai chover hoje no Tocantins?


### Screenshoot
![](https://i.ibb.co/4P6B6v9/Screenshot-3.png)
> Conversa com Sarah

![](https://i.ibb.co/gWNbvrj/Screenshot-5.png)
> Conversa com Sarah

Necessário criar uma conta no website https://www.climacell.co/ e https://developer.tomtom.com/, para ter acesso as devidas API(inseridas em app/actions.py), para poder coletar as informações do clima e coordenadas geográficas, respectivamente.

Este bot será sendo melhorado e será implementado em breve o server das actions, para fazer deploy no haruku e funcionar devidamente conforme nos prints no site: http://carolstoffel.epizy.com/

Foi testado o chatbot no computador local, ao rodar os seguintes comandos:
rasa train
rasa run actions
rasa run -m models --enable-api --cors “*” --debug (em outro cmd)

Executado o ngrok e executado o seguinte comando:
ngrok.exe http 5005

