import onnxruntime as ort
import joblib
import onnx
import skl2onnx
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

onnx_path = "model.onnx"

sess = None

def load_model():
    global sess
    sess = ort.InferenceSession(onnx_path)

def predict(X):
    if sess is None:
        load_model()
    inputs = {sess.get_inputs()[0].name: X.astype("float32")}
    return sess.run(None, inputs)[0]

def save_onnx_model(model):
    initial_type = [("input", FloatTensorType([None, model.n_features_in_]))]
    onnx_model = convert_sklearn(model, initial_types=initial_type)
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())