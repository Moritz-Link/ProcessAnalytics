## ProcessAnalytics


![alt text](https://github.com/Moritz-Link/ProcessAnalytics/blob/main/ProccesAnalyticsProject/ProcessAnalticsPlatform.png)

Frameworks and libraries used
 - PyTorch (torch)
 - PyTorch Geometric (torch_geometric)
 - Django
 - pandas
 - numpy

Overview
--------
ProcessAnalytics is a Django-based platform for exploring event logs as graphs and for running a Graph Neural Network (GNN) that predicts a case-level target ("repair_In5days"). The web UI lets you upload or view log files, inspect individual cases step-by-step, edit process step data, and (when available) run the trained GNN to get predictions.

Key design goals
 - Make event logs explorable and editable through a simple Django UI.
 - Represent each case as a graph and use a message-passing GNN to predict outcomes at the case level.
 - Keep preprocessing and model code together with the app so that the UI can load encoders and models for inference.

GNN architecture (high level)
------------------------------
The project converts each process instance (case) into a graph and applies a message-passing GNN to produce a single prediction per case. Important pieces:

 - Graph construction: nodes correspond to individual events / process steps. Directed edges typically represent the temporal sequence between events (e.g., event i -> event i+1) and may encode additional relations when available.
 - Node features: categorical attributes (for example ACTIVITY, SERVICEPOINT, DEVICETYPE) are encoded using saved encoders (found under `graphAPP1/gnn_models/`), and numeric features are included directly.
 - Message-passing backbone: implemented with PyTorch Geometric (torch_geometric). The model applies several graph-convolution / message-passing layers (the project code uses a custom module in `graphAPP1/gnn_models/model_gnn.py`) to aggregate local neighborhood information into node embeddings.
 - Readout and prediction: node embeddings are pooled (sum/mean/global pooling) into a graph-level vector and passed through an MLP classifier/regressor to predict `repair_In5days` for the entire case.

Training & artifacts
--------------------
- Training code and an exploratory notebook are included in `modelTraining.ipynb` at the repository root. That notebook shows preprocessing, graph construction, and model training.
- Trained model artifacts and encoders are stored (when present) under `ProccesAnalyticsProject/graphAPP1/gnn_models/` — e.g. `gnn_model.sav`, `gnn_model17`, and the encoder files. The Django app loads these for inference via the helper in `model_gnn.py`.
- Note: some trained model files can be large. If a model artifact is not present in the repository, re-training using `modelTraining.ipynb` will reproduce it (data is private — see below).

Using the app (developer quick start)
-----------------------------------
1. Create a Python environment and install core dependencies. Typical packages:

	- Django
	- torch
	- torch_geometric (PyTorch Geometric and its dependencies)
	- pandas
	- numpy
	- scikit-learn (for encoders / preprocessing)

2. From the project root run migrations and start the dev server:

	1. python manage.py migrate
	2. python manage.py createsuperuser  (optional, to access admin)
	3. python manage.py runserver

3. Open the web UI in your browser at http://localhost:8000/ (templates are in `ProccesAnalyticsProject/templates/`). Use the pages to upload or view logs and inspect cases. The graph visualizations and client-side interactions live in `ProccesAnalyticsProject/static/` (see `graphJS.js`, CSS files and images).

Running the GNN for inference
-----------------------------
- The Django app includes code to load encoders and the saved model for inference. See `ProccesAnalyticsProject/graphAPP1/gnn_models/model_gnn.py` for the loading and prediction helper.
- When a trained model artifact is present in `graphAPP1/gnn_models/`, the app will load it and produce predictions for cases (the UI exposes the relevant actions where implemented).

Data
----
- This repository contains example/preprocessed CSVs in `ProccesAnalyticsProject/static/data/` but the original raw data used for training is private.

Files & locations of interest
----------------------------
- `modelTraining.ipynb` — notebook that shows preprocessing, graph construction and model training.
- `ProccesAnalyticsProject/graphAPP1/gnn_models/` — encoder and model artifacts plus `model_gnn.py` (model loading & inference logic).
- `ProccesAnalyticsProject/graphAPP1/views.py` — web endpoints for listing and inspecting cases; integrates model inference where applicable.
- `ProccesAnalyticsProject/templates/` and `ProccesAnalyticsProject/static/` — frontend pages, JS and CSS used by the UI.

Extending or re-training the model
----------------------------------
- Reproduce preprocessing in `modelTraining.ipynb` to regenerate encoders and training datasets.
- Use PyTorch and PyTorch Geometric to experiment with different GNN layers (GraphConv, GATConv, SAGEConv, etc.), pooling strategies, and MLP heads.

Notes and limitations
---------------------
- The original data is private; the repository includes preprocessed examples only. If the large trained model is missing, re-running the notebook with your data is required.
- The web UI focuses on exploration and quick inference. For heavy batch prediction, extract graph features with the preprocessing notebook and run inference in a dedicated script.

Contact / model training
------------------------
 - Training notebook: `modelTraining.ipynb`
 - Architecture & runtime inference helpers: `ProccesAnalyticsProject/graphAPP1/gnn_models/model_gnn.py`




