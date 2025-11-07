from flask import Flask, render_template, request, jsonify
from google import genai
import settings

app = Flask(__name__)

# Configurar a API do Gemini
client = genai.Client(api_key=settings.GEMINI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Mensagem vazia'}), 400
        
        # Criar contexto para aprendizado de programação
        prompt = f"""Você é um professor de programação experiente e didático. 
        Sua missão é ajudar estudantes a aprender programação de forma clara e objetiva.
        
        Pergunta do aluno: {user_message}
        
        Forneça uma resposta educativa, com exemplos práticos quando relevante."""
        
        # Enviar mensagem para o Gemini
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        return jsonify({
            'response': response.text,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)