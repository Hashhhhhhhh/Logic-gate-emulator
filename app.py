from flask import Flask, render_template, request, jsonify
import numpy as np
import base64
import io
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to simulate quantum circuit (stub for demonstration)
def simulate_circuit(circuit):
    # For demonstration, let's create a dummy result
    num_states = 2 ** len(circuit.split())
    state = np.random.rand(num_states) + 1j * np.random.rand(num_states)
    state /= np.linalg.norm(state)  # Normalize the state

    # Create a plot to visualize the state
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(state)), np.abs(state)**2)
    plt.title('Quantum State Visualization')
    plt.xlabel('State Index')
    plt.ylabel('Probability Amplitude')
    plt.xticks(range(len(state)))

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()  # Close the plot

    return state, image_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    circuit_desc = data.get('circuit', '')

    if not circuit_desc:
        return jsonify({'error': 'No circuit provided', 'details': 'Please provide a valid circuit.'}), 400

    try:
        state, image_data = simulate_circuit(circuit_desc)
        state_serializable = [{'real': ampl.real, 'imag': ampl.imag} for ampl in state]

        return jsonify({
            'state': state_serializable,
            'image': image_data,
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'details': 'An error occurred during simulation.',
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
