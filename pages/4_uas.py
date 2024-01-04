import streamlit as st
import pandas as pd
import numpy as np

# Fungsi untuk Metode MOORA
def moora(matrix, weights, criteria_types):
    # Normalisasi matriks keputusan
    normalized = matrix.copy()
    for i, crit_type in enumerate(criteria_types):
        if crit_type == 'cost':
            normalized[:, i] = np.min(matrix[:, i]) / matrix[:, i]
        elif crit_type == 'benefit':
            normalized[:, i] = matrix[:, i] / np.max(matrix[:, i])

    # Mengalikan dengan bobot kriteria
    weighted = normalized * weights

    # Menjumlahkan hasil
    scores = np.sum(weighted, axis=1)

    return scores

# Fungsi untuk menampilkan visualisasi
def display_visualization(scores):
    # visualisasi
    scores_df = pd.DataFrame({'Alternatif': [f'Alternatif {i+1}' for i in range(len(scores))],
                              'Score': scores})
    st.bar_chart(scores_df.set_index('Alternatif'))

# Tampilan web dengan Streamlit
st.title('Sistem Pendukung Keputusan menggunakan Metode MOORA')

# Input data matriks keputusan
st.header('Masukkan Data Matriks Keputusan')
num_alternatives = st.number_input('Jumlah Alternatif:', min_value=2, step=1, value=3)
num_criteria = st.number_input('Jumlah Kriteria:', min_value=2, step=1, value=3)

criteria_types = []
weights = []

matrix_data = []
for i in range(num_criteria):
    crit_type = st.selectbox(f'Jenis Kriteria {i+1}:', options=['cost', 'benefit'])
    criteria_types.append(crit_type)
    weight = st.number_input(f'Bobot Kriteria {i+1} (0-1):', min_value=0.0, max_value=1.0, step=0.1)
    weights.append(weight)

    col_data = []
    for j in range(num_alternatives):
        col_data.append(st.number_input(f'Nilai Kriteria {i+1} Alternatif {j+1}:'))
    matrix_data.append(col_data)

matrix = np.array(matrix_data).T

if st.button('Hitung'):
    scores = moora(matrix, weights, criteria_types)
    ranking = np.argsort(scores)[::-1] + 1  # Urutan peringkat dari terbesar ke terkecil

    st.header('Hasil Perangkingan:')
    st.write('Hasil MOORA:', scores)

    ranking_df = pd.DataFrame({'Alternatif': [f'Alternatif {i+1}' for i in range(len(scores))],
                               'Score': scores,
                               'Ranking': ranking})
    st.write(ranking_df)

    display_visualization(scores)

