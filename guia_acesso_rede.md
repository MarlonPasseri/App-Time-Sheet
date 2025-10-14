# Guia de Acesso à Rede para o Sistema de Controle de Horas

Este guia detalha os passos necessários para configurar o sistema de controle de horas para que ele possa ser acessado por outros computadores na mesma rede local. Por padrão, quando você executa uma aplicação web localmente, ela geralmente só é acessível a partir do próprio computador (usando `localhost` ou `127.0.0.1`). Para permitir o acesso de outros dispositivos, é preciso configurar o servidor para "escutar" em todas as interfaces de rede disponíveis e, em alguns casos, ajustar as configurações de firewall.

## 1. Entendendo o Problema de Acesso

Quando um funcionário tenta acessar o sistema usando `http://localhost:5000` em seu próprio computador, e o servidor está rodando em outra máquina, a conexão falha. Isso ocorre porque `localhost` sempre se refere ao próprio computador do usuário. Para acessar o servidor em outra máquina, é necessário usar o endereço IP dessa máquina.

## 2. Configurando o Servidor Flask para Acesso Externo

O sistema de controle de horas, desenvolvido em Flask, já está configurado para aceitar conexões de qualquer endereço IP, o que é um passo crucial para o acesso em rede. No arquivo `src/main.py`, a linha que inicia o servidor geralmente se parece com:

```python
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
```

O parâmetro `host='0.0.0.0'` indica que o servidor Flask deve "escutar" em todas as interfaces de rede disponíveis no computador onde ele está sendo executado. Isso significa que ele está pronto para receber conexões de outros computadores na rede local.

## 3. Encontrando o Endereço IP do Computador Servidor

Para que outros computadores possam acessar o sistema, eles precisam saber o endereço IP do computador onde o servidor Flask está rodando. Veja como encontrar esse endereço:

### No Windows:

1.  Abra o Prompt de Comando (digite `cmd` na barra de pesquisa do Windows e pressione Enter).
2.  Digite `ipconfig` e pressione Enter.
3.  Procure por "Endereço IPv4" na seção do adaptador de rede que você está usando (por exemplo, "Adaptador Ethernet" ou "Adaptador de LAN sem Fio"). O número ao lado é o endereço IP do seu computador (ex: `192.168.1.100`).

### No Linux ou macOS:

1.  Abra o Terminal.
2.  Digite `ifconfig` (Linux, pode precisar instalar `net-tools`) ou `ip addr show` (Linux) ou `ipconfig getifaddr en0` (macOS para Wi-Fi, `en1` para Ethernet) e pressione Enter.
3.  Procure pelo endereço IP associado à sua interface de rede ativa (geralmente `eth0` para Ethernet ou `wlan0` para Wi-Fi no Linux, ou `en0`/`en1` no macOS). O endereço IP será algo como `192.168.1.100`.

## 4. Acessando o Sistema de Outro Computador

Com o endereço IP do computador servidor em mãos, o funcionário pode acessar o sistema abrindo um navegador web e digitando o seguinte endereço:

`http://[ENDEREÇO_IP_DO_SERVIDOR]:5000`

Substitua `[ENDEREÇO_IP_DO_SERVIDOR]` pelo endereço IP real que você encontrou no passo anterior. Por exemplo, se o IP for `192.168.1.100`, o endereço completo seria `http://192.168.1.100:5000`.

## 5. Lidando com o Firewall

Um firewall é um sistema de segurança que controla o tráfego de rede. Se o sistema ainda não estiver acessível após configurar o `host='0.0.0.0'` e usar o IP correto, é provável que o firewall do computador servidor esteja bloqueando a porta 5000.

### No Windows (Firewall do Windows Defender):

1.  Abra o "Painel de Controle" e vá para "Sistema e Segurança" > "Firewall do Windows Defender".
2.  Clique em "Permitir um aplicativo ou recurso através do Firewall do Windows Defender".
3.  Clique em "Alterar configurações" (pode ser necessário ter permissões de administrador).
4.  Role para baixo e procure pelo seu aplicativo Python ou, se não o encontrar, clique em "Permitir outro aplicativo...".
5.  Navegue até o executável do Python (`python.exe`) que está executando seu script Flask (geralmente em `C:\Users\SeuUsuario\AppData\Local\Programs\Python\PythonXX\python.exe`).
6.  Adicione-o e certifique-se de que as caixas "Privado" e "Público" estejam marcadas para permitir o acesso nas redes desejadas.

Alternativamente, você pode criar uma regra de porta de entrada:

1.  No Firewall do Windows Defender, clique em "Configurações avançadas".
2.  No painel esquerdo, clique em "Regras de Entrada".
3.  No painel direito, clique em "Nova Regra...".
4.  Selecione "Porta" e clique em "Avançar".
5.  Selecione "TCP" e em "Portas locais específicas", digite `5000`. Clique em "Avançar".
6.  Selecione "Permitir a conexão" e clique em "Avançar".
7.  Marque os perfis de rede aplicáveis (Domínio, Privado, Público) e clique em "Avançar".
8.  Dê um nome à regra (ex: "Acesso Flask 5000") e clique em "Concluir".

### No Linux (UFW - Uncomplicated Firewall, comum no Ubuntu):

1.  Abra o Terminal.
2.  Para permitir o tráfego na porta 5000, digite:
    `sudo ufw allow 5000/tcp`
3.  Verifique o status do firewall:
    `sudo ufw status`

### No macOS (Firewall integrado):

1.  Vá para "Preferências do Sistema" > "Segurança e Privacidade" > "Firewall".
2.  Clique no cadeado para fazer alterações e digite sua senha de administrador.
3.  Clique em "Opções do Firewall...".
4.  Clique no botão "+" para adicionar um aplicativo.
5.  Navegue até o executável do Python que está executando seu script Flask.
6.  Certifique-se de que a opção "Permitir conexões de entrada" esteja selecionada para o Python.

## 6. Testando a Conexão

Após realizar as configurações, execute o servidor Flask no computador principal e tente acessar o sistema a partir de outro computador na mesma rede usando o endereço IP e a porta (ex: `http://192.168.1.100:5000`). Se tudo estiver correto, a página inicial do sistema deverá ser carregada.

## 7. Considerações Finais

-   **Rede Local**: Este guia é para acesso dentro da mesma rede local (LAN). Para acesso via internet (WAN), seriam necessárias configurações adicionais no roteador (redirecionamento de portas), o que não é recomendado para aplicações sem segurança robusta e sem um domínio.
-   **Endereço IP Dinâmico**: A maioria das redes domésticas atribui endereços IP dinamicamente. Isso significa que o endereço IP do seu computador pode mudar com o tempo. Se o acesso parar de funcionar, verifique se o endereço IP do servidor não mudou.
-   **Segurança**: Expor uma aplicação na rede local aumenta ligeiramente a superfície de ataque. Certifique-se de que o sistema de login esteja funcionando corretamente e que as senhas sejam fortes.

Com este guia, você e seus funcionários devem conseguir acessar o sistema de controle de horas de diferentes computadores na rede local sem problemas.

