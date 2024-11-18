// Definição de pinos e variáveis
int trigPin = 9;
int echoPin = 10;
int ledVermelho = 5;
int ledAmarelo = 4;
int ledVerde = 3;
int buzzerPin = 6;
int botaoPin = 7;  // Pino do botão

long duration;
float distance;

// Variáveis para controle de tempo
unsigned long previousMillis = 0;  
const long interval = 500;  // Intervalo de 500 milissegundos

// Variável de controle de finalização do processo
bool finalizar = false;

void setup() {
  // Inicializa os pinos
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledVermelho, OUTPUT);
  pinMode(ledAmarelo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(botaoPin, INPUT_PULLUP);  // Configura o pino do botão como entrada com pull-up
  
  // Inicializa a comunicação serial
  Serial.begin(9600);
}

void loop() {
  unsigned long currentMillis = millis(); // Captura o tempo atual

  // Verifica se o botão foi pressionado (está em LOW devido ao resistor pull-up)
  if (digitalRead(botaoPin) == LOW) {
    finalizar = true;  // Altera a variável 'finalizar' para true quando o botão é pressionado
    Serial.println("Processo finalizado!");
  }

  // Verifica se o tempo do intervalo já passou (para medir a distância a cada 500 ms)
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;  // Atualiza o último tempo

    // Se o processo não foi finalizado, continua a medição de distância
    if (!finalizar) {
      // Gera um pulso no pino Trig para iniciar a medição
      digitalWrite(trigPin, LOW);  // Garante que o Trig esteja em LOW inicialmente
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH); // Envia um pulso de 10 microssegundos
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);  // Desliga o Trig

      // Lê o tempo do pulso de Echo
      duration = pulseIn(echoPin, HIGH);

      // Calcula a distância em centímetros (considerando a velocidade do som)
      distance = duration /50;  // Divido por 2 porque a distância percorrida é ida e volta

      // Exibe a distância no monitor serial
      Serial.print("Distância: ");
      Serial.print(distance);
      Serial.println(" cm");

      // Controle dos LEDs baseado na distância
      if (distance < 10) {
        // Se a distância for menor que 10 cm, acende o LED vermelho e ativa o buzzer
        digitalWrite(ledVermelho, HIGH);
        digitalWrite(ledAmarelo, LOW);
        digitalWrite(ledVerde, LOW);
        tone(buzzerPin, 1000);  // Emite um som de 1kHz no buzzer
      }
      else if (distance >= 10 && distance <= 30) {
        // Se a distancia estiver entre 10 cm e 30 cm, acende o LED amarelo
        digitalWrite(ledVermelho, LOW);
        digitalWrite(ledAmarelo, HIGH);
        digitalWrite(ledVerde, LOW);
        noTone(buzzerPin);  // Desliga o buzzer se a distância estiver entre 10 cm e 30 cm
      }
      else {
        // Se a distancia for maior que 30 cm, acende o LED verde
        digitalWrite(ledVermelho, LOW);
        digitalWrite(ledAmarelo, LOW);
        digitalWrite(ledVerde, HIGH);
        noTone(buzzerPin);  // Desliga o buzzer se a distância for maior que 30 cm
      }
    } else {
      // Se o processo foi finalizado, desliga todos os LEDs e o buzzer
      digitalWrite(ledVerde, LOW);
      digitalWrite(ledAmarelo, LOW);
      digitalWrite(ledVermelho, LOW);
      noTone(buzzerPin);  // Desliga o buzzer
    }
  }
}
