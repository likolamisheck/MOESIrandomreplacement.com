from flask import Flask, render_template, jsonify, request
from model import CacheModel

app = Flask(__name__)
cache_model = CacheModel(num_processors=4, memory_size=16, cache_size=4, num_sets=4, associativity=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perform_operation', methods=['POST'])
def perform_operation():
    data = request.get_json()
    processor_id = data['processor_id']
    operation = data['operation']
    address = data['address']

    if operation == 'read':
        cache_hit, cache_event_log = cache_model.read(processor_id, address)
    else:
        cache_hit, cache_event_log = cache_model.write(processor_id, address)

    cache_state = cache_model.get_cache_state()
    return jsonify({'cache_hit': cache_hit, 'cache_state': cache_state, 'cache_event_log': cache_event_log})

@app.route('/reset', methods=['POST'])
def reset():
    cache_model.reset()
    cache_state = cache_model.get_cache_state()
    return jsonify({'cache_state': cache_state})

if __name__ == '__main__':
    app.run(debug=True)
