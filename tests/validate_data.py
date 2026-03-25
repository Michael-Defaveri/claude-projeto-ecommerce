import pandas as pd
import numpy as np

# Load all CSV files
df_vendas = pd.read_csv('data/vendas_temporais_rows.csv')
df_clientes = pd.read_csv('data/clientes_segmentacao_rows.csv')
df_precos = pd.read_csv('data/precos_competitividade_rows.csv')

print('=== VENDAS_TEMPORAIS ===')
print(f'Shape: {df_vendas.shape}')
print(f'Columns: {list(df_vendas.columns)}')
print(f'Dtypes:\n{df_vendas.dtypes}')
print(f'Nulls:\n{df_vendas.isnull().sum()}')
print(f'Duplicates: {df_vendas.duplicated().sum()}')
print(f'Negative revenues: {(df_vendas["receita_total"] < 0).sum()}')
print(f'Negative quantities: {(df_vendas["quantidade_total"] < 0).sum()}')
print(f'ticket_medio sample check (receita/total_vendas):')
df_vendas['ticket_calc'] = df_vendas['receita_total'] / df_vendas['total_vendas']
diff = (df_vendas['ticket_calc'] - df_vendas['ticket_medio']).abs()
print(f'  Max diff: {diff.max():.6f}, Mean diff: {diff.mean():.6f}')
print(f'Date range: {df_vendas["data_venda"].min()} to {df_vendas["data_venda"].max()}')
print(f'Hour range: {df_vendas["hora_venda"].min()} to {df_vendas["hora_venda"].max()}')
print()

print('=== CLIENTES_SEGMENTACAO ===')
print(f'Shape: {df_clientes.shape}')
print(f'Columns: {list(df_clientes.columns)}')
print(f'Dtypes:\n{df_clientes.dtypes}')
print(f'Nulls:\n{df_clientes.isnull().sum()}')
print(f'Duplicates: {df_clientes.duplicated().sum()}')
print(f'Duplicate cliente_id: {df_clientes["cliente_id"].duplicated().sum()}')
print(f'Segment distribution:\n{df_clientes["segmento_cliente"].value_counts()}')
print(f'Negative revenues: {(df_clientes["receita_total"] < 0).sum()}')

# Verify segmentation rules: VIP >= 10000, TOP_TIER >= 5000, REGULAR < 5000
vip_check = df_clientes[df_clientes['segmento_cliente'] == 'VIP']['receita_total'] >= 10000
top_check = df_clientes[df_clientes['segmento_cliente'] == 'TOP_TIER']['receita_total'] >= 5000
reg_check = df_clientes[df_clientes['segmento_cliente'] == 'REGULAR']['receita_total'] < 5000
print(f'VIP >= 10000 rule: {vip_check.all()} ({vip_check.sum()}/{len(vip_check)})')
print(f'TOP_TIER >= 5000 rule: {top_check.all()} ({top_check.sum()}/{len(top_check)})')
print(f'REGULAR < 5000 rule: {reg_check.all()} ({reg_check.sum()}/{len(reg_check)})')

# Check ticket_medio
df_clientes['ticket_calc'] = df_clientes['receita_total'] / df_clientes['total_compras']
diff_c = (df_clientes['ticket_calc'] - df_clientes['ticket_medio'].astype(float)).abs()
print(f'ticket_medio check: max diff = {diff_c.max():.6f}')
print()

print('=== PRECOS_COMPETITIVIDADE ===')
print(f'Shape: {df_precos.shape}')
print(f'Columns: {list(df_precos.columns)}')
print(f'Dtypes:\n{df_precos.dtypes}')
print(f'Nulls:\n{df_precos.isnull().sum()}')
print(f'Duplicates: {df_precos.duplicated().sum()}')
print(f'Duplicate produto_id: {df_precos["produto_id"].duplicated().sum()}')
print(f'Price classification distribution:\n{df_precos["classificacao_preco"].value_counts()}')
print(f'Negative revenues: {(df_precos["receita_total"] < 0).sum()}')
print(f'Negative quantities: {(df_precos["quantidade_total"] < 0).sum()}')

# Verify diferenca_percentual_vs_media calculation
df_precos['diff_pct_calc'] = (df_precos['nosso_preco'] - df_precos['preco_medio_concorrentes']) / df_precos['preco_medio_concorrentes'] * 100
diff_p = (df_precos['diff_pct_calc'] - df_precos['diferenca_percentual_vs_media'].astype(float)).abs()
print(f'diferenca_percentual_vs_media check: max diff = {diff_p.max():.6f}')
print(f'nosso_preco range: {df_precos["nosso_preco"].min()} to {df_precos["nosso_preco"].max()}')
print(f'Categories: {df_precos["categoria"].unique()}')
