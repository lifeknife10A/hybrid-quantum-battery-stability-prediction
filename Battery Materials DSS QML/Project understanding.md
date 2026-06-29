# Project Understanding

Created: 2026-06-14

Folder studied:

- `Battery Materials DSS QML/Paper/`
- Pasted project reset text
- Existing prototype files in the main project folder

## 1. Final Project Title

India-Compliant Hybrid Quantum-Classical ML Framework for Lithium-Ion
Battery Material Discovery

This title is stronger than only saying "Quantum ML for battery
materials" because it includes:

- Battery material discovery
- Classical machine learning
- Hybrid quantum-classical machine learning
- India-specific feasibility
- Safety, environmental, commercial, and policy checks

## 2. Main Project Question

The project should answer this question:

Can we use classical ML and hybrid quantum-classical ML to identify
lithium-ion battery material candidates that are scientifically promising
and also feasible for India based on stability, safety, environmental,
commercial, and regulatory conditions?

So the final output should not only say:

`This compound is stable.`

It should say something closer to:

`This compound is predicted to be stable, belongs to a useful battery
material family, does not show obvious India feasibility red flags, and
is recommended, cautioned, or rejected.`

## 3. Best One-Line Understanding

This project is a decision-support system for battery material screening.

The ML/QML part predicts scientific stability.
The India feasibility filter checks practical usefulness.
The scoring system converts both into a final recommendation.

## 4. Core Problem

Lithium-ion battery material discovery is slow because traditional
research needs:

1. Chemical intuition
2. Lab synthesis
3. Testing
4. Failure analysis
5. Repeated experiments

Machine learning can reduce this time by screening many materials
computationally.

Quantum machine learning is added as an experimental research direction.
The quantum part should be presented honestly as a hybrid simulated
workflow, not as a guaranteed quantum advantage.

The new important point is India feasibility. A material is not useful
for this project if it is stable but toxic, difficult to source, heavily
regulated, commercially weak, or unsuitable for Indian battery policy.

## 5. Three Pillars

The project should stand on three pillars.

| Pillar | Meaning |
| --- | --- |
| Scientific feasibility | Is the material stable and battery relevant? |
| AI/QML prediction | Can classical ML and hybrid QML predict useful properties? |
| India feasibility | Is the material practical, safe, and policy-compatible for India? |

## 6. Final Objective

To develop an India-compliant hybrid quantum-classical machine learning
framework for screening lithium-ion battery materials by predicting
stability-related properties and ranking candidate compounds using a
combined feasibility score based on thermodynamic stability, battery
relevance, environmental safety, commercial availability, and Indian
regulatory considerations.

## 7. What Already Exists

The older prototype is useful, but it is only a starting point.

Existing project assets found:

- `SRM/lithium-ion batteries.csv`
- `SRM/Quantum_Battery_Stability_Notebook.ipynb`
- `Quantum_Battery_Stability_Notebook.ipynb`
- `SRM/Hybrid Quantum Classical ML Battery Materials Discovery Compressed.pdf`
- Report images showing dataset preview, model tables, circuit diagram,
  quantum feature matrix, and candidate ranking

The current CSV has 339 material rows plus a header.

Important columns in the current CSV:

- `Materials Id`
- `Formula`
- `Spacegroup`
- `Formation Energy (eV)`
- `E Above Hull (eV)`
- `Band Gap (eV)`
- `Nsites`
- `Density (gm/cc)`
- `Volume`
- `Has Bandstructure`
- `Crystal System`

Current notebook structure:

- Data loading
- Numeric conversion
- Classical baseline
- Feature compression
- Quantum encoding
- Hybrid quantum-classical learning
- Ranking by predicted stability

Important old result:

- In the notebook, the classical baseline performs better than the
  quantum-derived model.
- In the project report, the tuned classical model also performs slightly
  better than the tuned hybrid model.
- This should be presented honestly. The project demonstrates a hybrid
  QML workflow, not proven quantum advantage.

## 8. Main Weaknesses In The Old Version

| Weakness | Why It Matters |
| --- | --- |
| Dataset is small | 339 rows is only enough for a prototype. |
| No India feasibility filter | The system may recommend impractical materials. |
| No strong policy layer | Real-world India relevance is weak. |
| Classical model is stronger | QML must be compared honestly. |
| No clear reject/caution logic | Unsafe or unrealistic materials may pass. |
| Ranking is based mainly on stability | Final decision should include safety and feasibility. |

## 9. Target System Flow

The final system should work like this:

```text
Input compound formula or CSV
        |
        v
Extract elements and material family
        |
        v
Apply India feasibility rules
        |
        v
Predict energy above hull using ML/QML
        |
        v
Calculate final feasibility score
        |
        v
Rank compounds
        |
        v
Output Recommend / Caution / Reject
```

Example final output:

| Formula | Predicted E Above Hull | India Feasibility | Score | Decision |
| --- | ---: | --- | ---: | --- |
| LiFePO4 | 0.015 | Safe and feasible | 92 | Recommend |
| LiMn2O4 | 0.032 | Feasible with caution | 84 | Recommend |
| LiCoO2 | 0.041 | Cobalt supply/toxicity concern | 68 | Caution |
| Cd-based compound | 0.030 | Toxic heavy-metal concern | 15 | Reject |

## 10. Main Modules

The final project should have five main modules.

### Module 1: Literature And Policy Review

Purpose:

- Understand battery material discovery.
- Understand ML and QML in materials science.
- Understand Indian battery, mineral, recycling, and hazardous material
  policy.
- Convert documents into practical project rules.

Output:

- `Literature_Review_Matrix.xlsx`
- Government-policy source table
- Initial rule notes

### Module 2: Dataset Collection And Cleaning

Purpose:

- Move beyond the small 339-row demo dataset.
- Collect a larger lithium-containing material dataset.
- Keep only useful fields for stability prediction and ranking.

Good dataset targets:

- Minimum: 1000+ lithium-containing compounds
- Better: 5000+ inorganic lithium-containing compounds

Useful sources:

- Materials Project
- JARVIS
- OQMD
- AFLOW

Main target variable:

- `energy_above_hull`

### Module 3: India Feasibility Filter

Purpose:

- Add element-level and material-family-level checks.
- Flag materials that are scientifically stable but practically risky.
- Avoid claiming something is illegal unless a source clearly says so.

Preferred labels:

- `Allow`
- `Caution`
- `Needs regulatory review`
- `Reject for this project`

### Module 4: Classical ML And Hybrid QML Models

Purpose:

- Train classical models as a baseline.
- Build a hybrid QML feature-extraction workflow.
- Compare classical, quantum-only, and hybrid results.

Expected honest conclusion:

- Classical ML may perform better.
- Hybrid QML is still useful as a demonstrated research workflow.

### Module 5: Final Ranking Report Or Dashboard

Purpose:

- Convert predictions and feasibility rules into a final decision.
- Give a ranked list of materials.
- Show why each material was recommended, cautioned, or rejected.

## 11. Paper Folder Review

The `Paper` folder contains 20 PDF filenames, one JARVIS zip file, and
some duplicate PDFs. After checking file hashes, there are 15 unique PDF
sources.

Duplicate PDF pairs found:

- `Battery Waste Management Rules 2022.pdf`
  and `Battery-WasteManagementRules-2022.pdf`
- `E-Waste Rules 2022.pdf`
  and `e-waste_rules_2022.pdf`
- `Manufacture Storage & Import of Hazardous Chemical Rules 1989.pdf`
  and `Manufacture_Storage&Import_of_Hazardous_Chemical_Rules 1989.pdf`
- `Notice and Questionnaire for ACC.pdf`
  and `Notice-and-Questionnaire-for-ACC.pdf`
- `Need for Advanced Chemistry Cell Energy Storage in India.pdf`
  and `RMI-India-battery-report-v6-14092022.pdf`

### 11.1 National Critical Mission

Category:

- Indian policy
- Critical minerals

Main understanding:

- India is treating critical minerals as strategically important.
- Battery storage, EVs, clean energy, and manufacturing increase demand
  for lithium, cobalt, nickel, manganese, graphite, copper, and related
  minerals.
- The mission emphasizes domestic production, overseas mineral assets,
  recycling, research, and supply-chain security.

How to use it:

- Give policy justification for the India feasibility layer.
- Mark lithium, cobalt, nickel, manganese, graphite, and copper as
  strategically important.
- Treat some of these as supply-risk elements, not automatic rejects.

### 11.2 Critical Minerals For India

Category:

- Indian policy
- Critical mineral identification

Main understanding:

- India has identified critical minerals based on economic importance and
  supply risk.
- Clean energy and EV growth make minerals like lithium, cobalt, nickel,
  graphite, manganese, and rare earth elements important.

How to use it:

- Add supply-risk reasoning to the scoring system.
- Support caution labels for materials involving cobalt and nickel.
- Support the need for recycling and alternative materials.

### 11.3 National Mineral Policy 2019

Category:

- Indian mining and mineral policy

Main understanding:

- India wants mineral development to support domestic industry and reduce
  import dependency.
- The policy discusses sustainable mining, environmental protection,
  mineral conservation, recycling, research, and supply security.

How to use it:

- Support the commercial availability score.
- Support the environmental/recycling score.
- Support the idea that material selection should consider Indian supply
  and sustainability.

### 11.4 Need For Advanced Chemistry Cell Energy Storage In India

Category:

- India battery manufacturing
- ACC policy
- Commercial feasibility

Main understanding:

- India wants to build a domestic advanced chemistry cell battery
  manufacturing ecosystem.
- The report discusses ACC manufacturing, PLI support, raw-material
  risk, battery reuse, battery recycling, and battery chemistries.
- It names common lithium-ion battery families such as LCO, LFP, LMO,
  LTO, NCA, and NMC.

How to use it:

- Justify why this project focuses on battery material families.
- Use LFP, LMO, LTO, NMC, LCO, and NCA as family categories.
- Support raw-material risk scoring.
- Support recycling and second-life relevance.

### 11.5 Notice And Questionnaire For ACC

Category:

- Indian government consultation
- ACC manufacturing

Main understanding:

- The notice is about stakeholder consultation for re-bidding 20 GWh
  PLI-ACC capacity.
- It shows government interest in domestic advanced chemistry cell and
  battery manufacturing.
- It asks about domestic value addition, manufacturing setup, and
  component supply.

How to use it:

- Support the claim that India feasibility is relevant.
- Add domestic value addition as a commercial-policy concern.

### 11.6 Battery Waste Management Rules 2022

Category:

- Indian environmental rule
- Battery waste and recycling

Main understanding:

- Battery waste management is a required part of the battery ecosystem.
- The rules cover producers, recyclers, refurbishers, collection, and
  recovery of battery materials.
- Recycling and environmentally sound handling matter for final
  feasibility.

How to use it:

- Build environmental/recycling score.
- Give caution to materials that may create difficult battery waste.
- Add end-of-life handling as part of the final decision.

### 11.7 E-Waste Rules 2022

Category:

- Indian e-waste rule
- Environmental management

Main understanding:

- These rules cover electronic waste management, recycling, producer
  responsibilities, transportation, and accident reporting.
- They are not specifically a battery material discovery paper, but they
  help show India's broader waste-management framework.

How to use it:

- Support environmental caution logic.
- Use only as background unless the material enters electronic waste or
  battery electronics handling.

### 11.8 Hazardous And Other Wastes Rules 2016

Category:

- Indian hazardous waste rule

Main understanding:

- These rules cover hazardous waste handling, recycling, import/export,
  labeling, authorisation, and accident reporting.
- The text mentions hazardous constituents such as lead, cadmium,
  mercury, arsenic, nickel, cobalt, and related wastes in different
  schedules and contexts.

How to use it:

- Build caution/reject logic for toxic heavy-metal compounds.
- Do not say a compound is illegal only because an element appears.
- Use safer labels like `Reject for this project` or
  `Needs regulatory review`.

### 11.9 Manufacture, Storage And Import Of Hazardous Chemical Rules 1989

Category:

- Indian hazardous chemical rule

Main understanding:

- These rules define hazardous chemicals and require safety data,
  labeling, accident planning, and import-related safeguards.
- The rules focus on chemical handling and major accident hazards.

How to use it:

- Support the `Needs regulatory review` label.
- Use for safety and handling risk, not for direct material performance.

### 11.10 AFLOW Paper

Category:

- Dataset/database paper
- High-throughput materials discovery

Main understanding:

- AFLOW is a high-throughput framework for computing crystal structure
  properties of inorganic compounds.
- It is based on systematic DFT calculations and database generation.

How to use it:

- Justify using high-throughput computed materials databases.
- Use AFLOW as a possible external data source.

### 11.11 JARVIS Zip

Category:

- Dataset/tool source

Main understanding:

- JARVIS-Tools is an open-access package for atomistic data-driven
  materials design.
- It supports DFT data, materials descriptors, ML workflows, and database
  access.
- The included documentation lists datasets such as `dft_3d`, `mp_3d`,
  `oqmd_3d`, `aflow2`, and others.

How to use it:

- Use JARVIS as a possible dataset source.
- Use it to download materials data and descriptors if needed.
- Keep it as a serious alternative if Materials Project access is hard.

### 11.12 Energy And AI

Category:

- ML in energy materials

Main understanding:

- ML can speed up energy material discovery by replacing or reducing
  slow trial-and-error screening.
- The paper discusses databases, feature engineering, ML algorithms, and
  applications in battery materials.
- It also highlights that battery data can be limited and that domain
  knowledge matters.

How to use it:

- Support the classical ML pipeline.
- Support feature engineering from material properties.
- Support combining DFT data, ML, and expert/domain rules.

### 11.13 Machine Learning For Molecular And Materials Science

Category:

- General ML materials science review

Main understanding:

- ML can accelerate design, synthesis, characterization, and application
  of molecules and materials.
- Materials science is suitable for ML because there are many candidate
  structures and properties to screen.

How to use it:

- Use in the literature review background.
- Support why ML is valid for materials discovery.

### 11.14 Scaling Deep Learning For Materials Discovery

Category:

- Advanced ML for materials discovery

Main understanding:

- Large graph-network models can scale materials discovery.
- The paper shows the importance of larger datasets and modern deep
  learning for finding stable materials.
- This is beyond the first student implementation, but it supports future
  direction.

How to use it:

- Explain why a larger dataset is needed.
- Use GNNs as a future-work direction, not the first required model.

### 11.15 Quantum Machine Learning For Lithium-Ion Battery Materials Discovery

Category:

- Current project report
- QML prototype

Main understanding:

- The earlier project already built a compact hybrid workflow.
- It used data preprocessing, feature selection, quantum encoding,
  quantum probability features, and model comparison.
- The report says the tuned classical baseline had RMSE 0.023174 and
  R2 0.453942, while the tuned hybrid model had RMSE 0.024215 and
  R2 0.403739.
- The report correctly admits that the hybrid model did not outperform
  the classical baseline.

How to use it:

- Keep it as the base prototype.
- Improve it with larger data and India feasibility rules.
- Present QML as experimental feature extraction.

### 11.16 AGILE Hand-Object Interaction Reconstruction

Category:

- Computer vision
- Agentic generation

Main understanding:

- This paper is about hand-object reconstruction from video.
- It is not directly related to lithium-ion battery materials,
  materials databases, QML, or Indian battery policy.

How to use it:

- Do not use it as a core source for this project.
- Keep it archived unless a separate agentic workflow explanation is
  needed later.

## 12. Literature Matrix Grain

For each paper or government document, the literature matrix should not
be a long essay.

Use one row per source.

Recommended columns:

- Title
- Year
- Source
- Category
- Main idea
- Dataset used
- Target property
- Method
- Key finding
- Limitation
- How we use it

Then create rule-level tables from the documents.

Example:

| Document | Key Finding | Project Use |
| --- | --- | --- |
| Battery Waste Management Rules 2022 | Battery recovery and recycling matter | Environmental score |
| Critical Minerals for India | Lithium, cobalt, nickel, graphite, manganese have supply importance | Supply-risk score |
| AFLOW paper | High-throughput DFT data supports material screening | Dataset source |

## 13. India Feasibility Filter

The India feasibility filter should work at two levels:

1. Element level
2. Compound-family level

### 13.1 Element-Level Draft

This is an initial student-level draft. It should later be converted into
`India_Feasibility_Rules.csv`.

| Element | Draft Status | Reason |
| --- | --- | --- |
| Li | Allow | Core lithium-ion battery element, but supply should be tracked. |
| Fe | Allow | Common and useful in LFP materials. |
| P | Allow | Useful in LFP materials. |
| O | Allow | Common in oxide battery materials. |
| Ti | Allow | Useful in LTO materials. |
| Si | Allow | Relevant for anode and silicate materials. |
| C | Allow | Relevant for graphite/anode materials. |
| Al | Allow | Relevant in NCA and current collector context. |
| Mn | Allow/Caution | Battery relevant, but still a critical/supply-aware element. |
| Graphite/C | Allow/Caution | Battery relevant and critical for supply-chain planning. |
| Co | Caution | Battery relevant but has cost, supply, and toxicity concerns. |
| Ni | Caution | Battery relevant but has cost, supply, and handling concerns. |
| V | Caution | Useful in some batteries, but toxicity/handling needs care. |
| F | Caution | Fluorinated compounds may need careful safety review. |
| Pb | Reject for this project | Toxic heavy-metal concern. |
| Cd | Reject for this project | Toxic heavy-metal concern. |
| Hg | Reject for this project | Highly toxic concern. |
| As | Reject for this project | Toxic/metalloid concern. |
| Radioactive elements | Reject for this project | Not suitable for a student screening project. |

Important rule:

Do not write `illegal` unless a government source clearly says that exact
use is banned. For this project, use safer labels like:

- `Caution`
- `Needs regulatory review`
- `Reject for this project`

### 13.2 Compound-Family Draft

| Family | Draft Status | Reason |
| --- | --- | --- |
| LFP: Li-Fe-P-O | Recommend | Strong India-friendly candidate family. |
| LMO: Li-Mn-O | Recommend/Caution | Battery relevant, but manganese handling/supply should be noted. |
| LTO: Li-Ti-O | Recommend | Battery relevant and generally safer than cobalt-rich chemistries. |
| Li-Si-O | Recommend/Caution | Relevant for lithium silicates and possible battery research. |
| NMC: Li-Ni-Mn-Co-O | Caution | Useful but cobalt/nickel supply and safety concerns exist. |
| LCO: Li-Co-O | Caution | Cobalt concern. |
| Pb/Cd/Hg/As compounds | Reject for this project | Toxic heavy-metal concern. |

## 14. Dataset Plan

The current 339-row dataset should be called a prototype dataset.

The final dataset should have these stages:

1. Raw materials dataset
2. Lithium-only dataset
3. Battery-relevant filtered dataset
4. India-feasible tagged dataset

Recommended files:

- `raw_materials_dataset.csv`
- `lithium_materials_dataset.csv`
- `battery_relevant_dataset.csv`
- `india_tagged_dataset.csv`

Minimum useful columns:

- `formula`
- `elements`
- `formation_energy_per_atom`
- `energy_above_hull`
- `band_gap`
- `density`
- `volume`
- `space_group`
- `crystal_system`
- `nsites`
- `is_stable`

Main target:

- `energy_above_hull`

Practical interpretation:

| Energy Above Hull | Meaning |
| ---: | --- |
| 0 eV/atom | Stable |
| 0 to 0.05 eV/atom | Very promising or near stable |
| 0.05 to 0.10 eV/atom | Possibly metastable |
| Greater than 0.10 eV/atom | Lower priority |

These are practical screening thresholds, not strict laws.

## 15. Classical ML Plan

Classical ML is required because it is the baseline.

Main task:

- Predict `energy_above_hull`

Optional second task:

- Predict `is_stable`

Start with simple models:

- Linear Regression
- Ridge Regression
- Random Forest
- Gradient Boosting

Then improve if time permits:

- XGBoost
- LightGBM
- CatBoost

Main metrics:

- RMSE
- MAE
- R2

For classification:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

For this project, precision is important because recommending a bad
material is worse than missing one good material.

## 16. Hybrid QML Plan

The QML part should be simple and honest.

Suggested workflow:

```text
Cleaned material features
        |
        v
Scaling
        |
        v
PCA or feature selection
        |
        v
4 selected features
        |
        v
4-qubit quantum circuit
        |
        v
Quantum measurement
        |
        v
Quantum feature table
        |
        v
Classical regressor
```

Recommended starting point:

- 4 qubits
- RY encoding
- CNOT entanglement
- Measurement probabilities
- Gradient Boosting or Random Forest on quantum features

Then compare:

| Setup | Meaning |
| --- | --- |
| Classical only | Normal ML on classical features |
| Quantum only | Model trained only on quantum features |
| Hybrid combined | Classical features plus quantum features |

Expected statement:

The hybrid QML model demonstrates quantum feature extraction, but it may
not outperform a strong classical model on simulated circuits and limited
data.

## 17. Final Feasibility Score

The final ranking should not depend only on predicted stability.

Suggested score:

```text
Final Feasibility Score =
0.40 * Stability Score
+ 0.20 * Battery Relevance Score
+ 0.20 * India Compliance Score
+ 0.10 * Cost Availability Score
+ 0.10 * Environmental Safety Score
```

Decision thresholds:

| Final Score | Decision |
| ---: | --- |
| 80 to 100 | Recommend |
| 60 to 79 | Caution |
| Below 60 | Reject |
| Any hard-reject element | Reject regardless of score |

Simple decision rule:

```text
If hard reject element is present:
    Decision = Reject
Else if predicted energy above hull is very high:
    Decision = Reject
Else if final score >= 80:
    Decision = Recommend
Else if final score >= 60:
    Decision = Caution
Else:
    Decision = Reject
```

## 18. Suggested Project Folder Structure

Use this structure for the reset version:

```text
India_Compliant_QML_Battery_Discovery/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── rules/
│   ├── India_Feasibility_Rules.csv
│   └── Battery_Material_Family_Rules.csv
├── notebooks/
│   ├── 01_literature_policy_matrix.ipynb
│   ├── 02_dataset_collection.ipynb
│   ├── 03_data_cleaning_eda.ipynb
│   ├── 04_classical_ml_baseline.ipynb
│   ├── 05_qml_feature_extraction.ipynb
│   ├── 06_hybrid_model_comparison.ipynb
│   └── 07_final_ranking_demo.ipynb
├── src/
│   ├── data_loader.py
│   ├── formula_parser.py
│   ├── india_filter.py
│   ├── feature_engineering.py
│   ├── classical_models.py
│   ├── quantum_features.py
│   ├── scoring.py
│   └── ranking.py
├── results/
│   ├── model_results.csv
│   ├── final_ranked_materials.csv
│   └── figures/
├── reports/
│   ├── literature_review_matrix.xlsx
│   ├── final_report.docx
│   └── final_presentation.pptx
└── references/
    ├── government_policy/
    ├── dataset_papers/
    ├── ml_papers/
    └── qml_papers/
```

## 19. Immediate Next Steps

Do these first:

1. Create the reset project folder structure.
2. Create `Literature_Review_Matrix.xlsx`.
3. Create `India_Feasibility_Rules.csv`.
4. Convert the paper notes in this file into the literature matrix.
5. Build the first element rule table.
6. Choose the final dataset source.
7. Do not start QML again until the dataset and India filter are clear.

## 20. Eight-Week Plan

| Week | Work | Output |
| --- | --- | --- |
| 1 | Problem statement and document collection | Problem statement, source list |
| 2 | Literature review and India rules | Literature matrix, rule table |
| 3 | Dataset collection | Raw and filtered datasets |
| 4 | Data cleaning and EDA | Cleaned data, EDA notebook |
| 5 | Classical ML | Baseline notebook, model table |
| 6 | QML and hybrid model | Quantum features, hybrid results |
| 7 | Feasibility scoring | Ranked materials table |
| 8 | Report and presentation | Final report, PPT, README |

## 21. Final Deliverables

Required:

- Literature review matrix
- Government-policy source table
- India feasibility rule table
- Larger lithium material dataset
- Cleaned dataset
- EDA notebook
- Classical ML notebook
- QML feature extraction notebook
- Hybrid model notebook
- Model comparison table
- Final feasibility score table
- Ranked material recommendations
- Final report
- PPT
- GitHub README

Optional:

- Streamlit dashboard
- Saved model files
- Extra visual dashboard

## 22. Final Project Story

The project should be explained like this:

Earlier, the project only predicted battery-material stability using
classical ML and hybrid QML. After reviewing the project direction, the
scope is being reset into an India-compliant material discovery pipeline.
The new system will first study research and Indian policy documents,
then build an India feasibility filter, use a larger lithium-material
dataset, train classical and hybrid QML models, and finally rank
materials as Recommend, Caution, or Reject.

This makes the project more realistic because it does not recommend a
material only because the predicted stability is good. It also checks
whether the material is practical for Indian battery use.

## 23. Important Caution

This project should not make legal claims unless they are directly
supported by a source.

Safer wording:

- `Caution`
- `Needs regulatory review`
- `Reject for this project`
- `Not preferred for student-level recommendation`

Avoid unsafe wording:

- `Illegal`
- `Banned`
- `Always safe`
- `Guaranteed commercially viable`

## 24. Final Understanding

The strongest version of this project is not only a prediction model.

It is a practical screening and ranking framework.

The final system should combine:

1. Scientific stability prediction
2. Battery material family identification
3. India policy and feasibility checks
4. Environmental and recycling awareness
5. Final material ranking

That is the main direction for the reset project.
