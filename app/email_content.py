def get_email_body(race_distance):
    email_body = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            line-height: 1.6;
        }
        .container {
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 5px;
        }
        h1 {
            font-size: 24px;
            text-align: center;
            color: #333;
        }
        p {
            font-size: 16px;
            color: #333;
        }
        .signature {
            text-align: right;
            font-style: italic;
        }
    </style>
    </head>
    <body>
        <div class="container">
            <h1>Балкан Ултра - ${race_distance}</h1>
            <p>Вашата регистрация за Балкан Ултра - ${race_distance} беше успешна! Ще Ви очакваме на 5 август 2023г на хижа Плевен!</p>
            <p>Ако вашата регистрация е за дългото трасе и очаквайте да бъдете одобрен до 7 дневен срок. Ако до тогава не виждате вашето име на сайта, моля проверете дали покривате изискванията за участие и ако сте изпратили нужните линкове към резултати се свържете с нас.</p>
            <p class="signature">С уважение, Росен и Иван.</p>
        </div>
    </body>
    </html>
    """.format(race_distance=race_distance)

    return email_body