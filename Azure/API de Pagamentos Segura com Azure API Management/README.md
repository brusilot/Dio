API de Pagamentos Segura com Azure API Management

 - Como criar método de proteção à Azure API utilizando OAuth

   Cliente pedirá o Token para o Azure AD e com o Bearer Token conseguirá chamar a API


 - Criar um API Management Service  (https://learn.microsoft.com/en-us/azure/api-management/get-started-create-service-instance)

 - WebApp
    - Api/Cors -> Enable , Allowed Origin > limitar para o Gateway URL do API Management criado anteriormente
    - Podemos limitar o acesso criando uma VNet também

 - APIMgmt > API (Selecionar WebApp ou Azure Function dependendo do que criou, e selecionar o criado anteriormente)
    - Adiconar Policies de reroute se quiser
    - Fazer configuração base da assinatura (Header name x-api-key)
        - "x-" é padrão do mercado de marcar tudo que não é padrão da API
    - APIs > Susbcription, criar nova subscription
    - APIs > APIs > Seleciona a API criada > Allow cross-origin resource sharing (CORS)
    - APIs > APIs > Seleciona a API criada > Validate JWT
    [Dentro do MS AD > Pegar/Criar o APP Registration > nome:app-gateway-xpto > pegar o client id, pegar a url de token em "endpoints" e OpenID Connect metada document
    Criar novo secret dentro de Manage>"Certificates & Secrets"> criar novo secret]
    - Voltando para o Validate JWT: Abrir aba "Full" > escolher se virá no Token o Header, o nome da variável, httpcode de falha e mensagem
    - Configurando a AUD 
        -app-gateway-xpto>Manage>Expose an API> Add a scope > e preencher os valores

    - Pegar o token chamando o endpoint de token pego acima
    - colocar como header o AUD criado acima ao pegar o Token
