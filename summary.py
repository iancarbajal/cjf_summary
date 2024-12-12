import openai
import os
from tqdm import tqdm
import sys
from read import extract_text


def process_chunk(prompt, chunk, output_path, model):
    with open(output_path, 'a') as output_file:

        full_prompt = (
            "Eres un asistente legal experto en derecho mexicano. Tu tarea es analizar un texto judicial "
            "y realizar las siguientes tareas:\n\n"
            "1. Identificar claramente 'la litis' del texto, que es la cuestión central o el conflicto principal del caso.\n"
            "2. Generar un resumen detallado de mínimo 300 palabras y máximo 1000, en español, que incluya:\n"
            "   - Contexto del caso y antecedentes relevantes.\n"
            "   - Partes involucradas y su posición.\n"
            "   - Análisis de los argumentos principales presentados.\n"
            "   - Decisiones, conclusiones o resoluciones relevantes.\n"
            "3. Extraer los nombres de los magistrados y personas importantes mencionadas en el texto.\n"
            "4. Identificar la duración del caso si se menciona (desde el inicio del proceso hasta la resolución).\n\n"
            "Texto judicial: \n\n"
            f"{' '.join(chunk)}\n\n"
            "Por favor, responde en el siguiente formato, asegurándote de que cada sección tenga al menos 50 palabras:\n\n"
            "---\n"
            "**Litis:** [Describe aquí la litis identificada, con al menos 50 palabras explicando en qué consiste el conflicto principal y su relevancia en el caso.]\n\n"
            "**Resumen detallado:**\n"
            "**Contexto y antecedentes:** [Explica el contexto y los antecedentes relevantes del caso con al menos 50 palabras.]\n"
            "**Partes involucradas y posición:** [Identifica a las partes y explica brevemente su posición con al menos 50 palabras.]\n"
            "**Análisis de argumentos:** [Resume los argumentos principales que se presentan en el texto judicial con al menos 50 palabras.]\n"
            "**Resoluciones:** [Describe las decisiones, conclusiones o resoluciones relevantes del caso con al menos 50 palabras.]\n\n"
            "**Magistrados y personas importantes:** [Lista los nombres de los magistrados, jueces u otras personas destacadas mencionadas en el texto.]\n"
            "**Duración del caso:** [Indica la duración del caso o las fechas importantes si se encuentran disponibles.]\n"
            "---"
        )

        messages = [{'role': 'system', 'content': 'I am a helpful assistant.'},
                {'role': 'user', 'content': full_prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages)
        response = response['choices'][0]['message']['content']
        output_file.write(response + '\n\n')

def split_file_to_chunks(prompt, input_path, output_path, chunk_size, model):
    with open(input_path, 'r') as file:
        content = extract_text(input_path)
        words = content.split()

        for i in tqdm(range(0, len(words), chunk_size)):
            chunk = words[i:i+chunk_size]
            process_chunk("", chunk, output_path, model)

if __name__ == '__main__':
    #KEY de OPENAI
    openai.api_key_path = "OPENAI_KEY.txt"
    # TODO:  checks para saber que la llave es valida
    model = 'gpt-3.5-turbo'

    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    input_path = sys.argv[1]
    if os.path.exists(input_path) == False:
        print(f'`{input_path}` can\'t be found.')
        exit()

    output_path = f'{sys.argv[1]}_output.txt'
        
    chunk_size = 12000
            
    split_file_to_chunks("",input_path, output_path, chunk_size, model)
