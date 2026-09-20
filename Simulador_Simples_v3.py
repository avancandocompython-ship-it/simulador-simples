import streamlit as st

st.set_page_config(
    page_title="Simulador Simples Puro x Híbrido",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Simulador – Simples Puro x Híbrido")
st.caption("Simulação gerencial 2027/2028")

# ============================================================
# FUNÇÕES
# ============================================================

def aliquota_efetiva(rbt12, tabela):
    """Calcula a alíquota efetiva conforme a faixa do Simples."""
    if rbt12 <= 0:
        return 0.0

    for limite, aliquota, parcela_deduzir in tabela:
        if rbt12 <= limite:
            return max(
                0.0,
                ((rbt12 * aliquota) - parcela_deduzir) / rbt12
            )

    return 0.0


def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ============================================================
# TABELAS DOS ANEXOS
# ============================================================

ANEXO_I = [
    (180000, 0.040, 0),
    (360000, 0.073, 5940),
    (720000, 0.095, 13860),
    (1800000, 0.107, 22500),
    (3600000, 0.143, 87300),
    (4800000, 0.189, 378000),
]

ANEXO_II = [
    (180000, 0.045, 0),
    (360000, 0.078, 5940),
    (720000, 0.100, 13860),
    (1800000, 0.112, 22500),
    (3600000, 0.147, 85500),
    (4800000, 0.299, 720000),
]

ANEXO_III = [
    (180000, 0.060, 0),
    (360000, 0.112, 9360),
    (720000, 0.135, 17640),
    (1800000, 0.160, 35640),
    (3600000, 0.210, 125640),
    (4800000, 0.329, 648000),
]

ANEXO_IV = [
    (180000, 0.045, 0),
    (360000, 0.090, 8100),
    (720000, 0.102, 12420),
    (1800000, 0.140, 39780),
    (3600000, 0.220, 183780),
    (4800000, 0.329, 828000),
]

ANEXO_V = [
    (180000, 0.155, 0),
    (360000, 0.180, 4500),
    (720000, 0.195, 9900),
    (1800000, 0.205, 17100),
    (3600000, 0.230, 62100),
    (4800000, 0.304, 540000),
]

TABELAS = {
    "Anexo I": ANEXO_I,
    "Anexo II": ANEXO_II,
    "Anexo III": ANEXO_III,
    "Anexo IV": ANEXO_IV,
    "Anexo V": ANEXO_V,
}


# ============================================================
# 1. IDENTIFICAÇÃO
# ============================================================

st.header("1. Identificação")

# Agora são campos digitáveis.
# Não existe mais Discatel ou CNPJ fixo.

col1, col2 = st.columns(2)

with col1:
    empresa = st.text_input(
        "Nome da empresa",
        value="",
        placeholder="Digite o nome da empresa"
    )

with col2:
    cnpj = st.text_input(
        "CNPJ",
        value="",
        placeholder="Digite o CNPJ"
    )


# ============================================================
# 2. ENQUADRAMENTO DA EMPRESA
# ============================================================

st.header("2. ENQUADRAMENTO DA EMPRESA")

st.info(
    "INFORME AQUI O ANEXO DA EMPRESA. Esta seleção define qual alíquota "
    "será usada no cálculo do DAS. Na planilha: B41 = Anexo I, "
    "B42 = Anexo II, B43 = Anexo III, B44 = Anexo IV e B45 = Anexo V. "
    "A B46 corresponde ao valor do DAS."
)

anexo_selecionado = st.selectbox(
    "➡️ SELECIONE O ANEXO DA EMPRESA",
    [
        "Selecione o Anexo",
        "Anexo I",
        "Anexo II",
        "Anexo III",
        "Anexo IV",
        "Anexo V",
    ],
    index=0
)

if anexo_selecionado == "Selecione o Anexo":
    st.warning(
        "⚠️ Selecione o Anexo da empresa antes de analisar o resultado."
    )

# ============================================================
# 3. DADOS TRIBUTÁRIOS
# ============================================================

st.header("3. Dados Tributários Atuais")

col1, col2 = st.columns(2)

with col1:
    rbt12 = st.number_input(
        "RBT12",
        min_value=0.0,
        value=0.0,
        step=1000.00
    )

with col2:
    receita_mes = st.number_input(
        "Receita do mês",
        min_value=0.0,
        value=0.0,
        step=1000.00
    )

st.subheader("Receita por Anexo")

col1, col2, col3 = st.columns(3)

with col1:
    receita_anexo1 = st.number_input(
        "Receita Anexo I",
        min_value=0.0,
        value=0.0
    )

    receita_anexo2 = st.number_input(
        "Receita Anexo II",
        min_value=0.0,
        value=0.0
    )

with col2:
    receita_anexo3 = st.number_input(
        "Receita Anexo III",
        min_value=0.0,
        value=0.0
    )

    receita_anexo4 = st.number_input(
        "Receita Anexo IV",
        min_value=0.0,
        value=0.0
    )

with col3:
    receita_anexo5 = st.number_input(
        "Receita Anexo V",
        min_value=0.0,
        value=0.0
    )

receita_total = (
    receita_anexo1
    + receita_anexo2
    + receita_anexo3
    + receita_anexo4
    + receita_anexo5
)

st.metric(
    "Receita total dos Anexos",
    moeda(receita_total)
)


# ============================================================
# 4. PERFIL DAS VENDAS
# ============================================================

st.header("4. Perfil das Vendas")

col1, col2, col3 = st.columns(3)

with col1:
    total_nf = st.number_input(
        "Total das NF de saída informadas",
        min_value=0.0,
        value=0.0
    )

with col2:
    receita_b2b = st.number_input(
        "Receita B2B – empresas privadas",
        min_value=0.0,
        value=0.0
    )

with col3:
    receita_pf = st.number_input(
        "Receita – pessoas físicas",
        min_value=0.0,
        value=0.0
    )

if total_nf > 0:
    percentual_b2b = receita_b2b / total_nf
    percentual_pf = receita_pf / total_nf
    percentual_b2c = max(
        0.0,
        1.0 - percentual_b2b - percentual_pf
    )
else:
    percentual_b2b = 0.0
    percentual_pf = 0.0
    percentual_b2c = 0.0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("% B2B", f"{percentual_b2b:.2%}")

with col2:
    st.metric("% B2C", f"{percentual_b2c:.2%}")

with col3:
    st.metric("% Pessoa Física", f"{percentual_pf:.2%}")


# ============================================================
# 5. AQUISIÇÕES
# ============================================================

st.header("5. Aquisições – Base de Créditos")

col1, col2 = st.columns(2)

with col1:
    entradas_simples = st.number_input(
        "Fornecedores / prestadores Simples ou MEI",
        min_value=0.0,
        value=0.0
    )

with col2:
    entradas_normal = st.number_input(
        "Fornecedores / prestadores Regime Normal",
        min_value=0.0,
        value=0.0
    )

total_entradas = entradas_simples + entradas_normal

st.metric(
    "Total de entradas",
    moeda(total_entradas)
)

col1, col2 = st.columns(2)

with col1:
    potencial_baixo = st.number_input(
        "Potencial de crédito: nenhum e/ou baixo",
        min_value=0.0,
        value=0.0
    )

with col2:
    potencial_medio_alto = st.number_input(
        "Potencial de crédito: médio/alto/analisar",
        min_value=0.0,
        value=0.0
    )


# ============================================================
# 6. PREMISSAS 2027/2028
# ============================================================

st.header("6. Simulação Indicativa 2027/2028 – Premissas Editáveis")

col1, col2, col3 = st.columns(3)

with col1:
    cbs = st.number_input(
        "CBS – premissa de planejamento",
        min_value=0.0,
        value=0.0921,
        format="%.4f"
    )

with col2:
    ibs = st.number_input(
        "IBS 2027 – premissa",
        min_value=0.0,
        value=0.001,
        format="%.4f"
    )

with col3:
    reducao = st.number_input(
        "Redução de IBS + CBS",
        min_value=0.0,
        max_value=1.0,
        value=0.30,
        format="%.2f"
    )

ibs_cbs = (cbs + ibs) * (1 - reducao)

st.metric(
    "Alíquota IBS + CBS considerada no regime regular",
    f"{ibs_cbs:.2%}"
)


# ============================================================
# 7. PROJEÇÃO
# ============================================================

st.header("7. Projeção")

receita_referencia = receita_total
receita_anual = receita_referencia * 12

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Receita mensal de referência",
        moeda(receita_referencia)
    )

with col2:
    st.metric(
        "Receita 2027 projetada",
        moeda(receita_anual)
    )


# ============================================================
# 8. CÁLCULO DAS ALÍQUOTAS
# ============================================================

aliquotas = {
    nome: aliquota_efetiva(receita_anual, tabela)
    for nome, tabela in TABELAS.items()
}

a1 = aliquotas["Anexo I"]
a2 = aliquotas["Anexo II"]
a3 = aliquotas["Anexo III"]
a4 = aliquotas["Anexo IV"]
a5 = aliquotas["Anexo V"]

# A seleção do Anexo agora determina qual alíquota será utilizada
# no cálculo principal do DAS.

aliquota_selecionada = aliquotas.get(anexo_selecionado, 0.0)

# Valor do DAS = receita anual x alíquota efetiva do Anexo selecionado.
das_puro = receita_anual * aliquota_selecionada


# ============================================================
# 9. IBS + CBS
# ============================================================

credito_estimado = potencial_medio_alto * ibs

# Mantida a lógica de referência da planilha:
# IBS/CBS somente quando a receita anual ultrapassa R$ 3,6 milhões.

if receita_anual > 3_600_000:
    ibs_cbs_bruto = receita_anual * ibs * (1 - reducao)
    creditos_ibs_cbs = potencial_medio_alto * ibs
else:
    ibs_cbs_bruto = 0.0
    creditos_ibs_cbs = 0.0

ibs_cbs_liquido = max(
    0.0,
    ibs_cbs_bruto - creditos_ibs_cbs
)

carga_total = das_puro + ibs_cbs_liquido


# ============================================================
# 10. COMPARAÇÃO
# ============================================================

st.header("8. Comparação – Cenário de Referência")

st.write(f"**Empresa:** {empresa}")
st.write(f"**CNPJ:** {cnpj}")
st.write(f"**Anexo selecionado:** {anexo_selecionado}")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Simples Puro")

    st.metric(
        "Alíquota efetiva",
        f"{aliquota_selecionada:.2%}"
    )

    st.metric(
        "Valor do DAS",
        moeda(das_puro)
    )

with col2:
    st.subheader("IBS + CBS")

    st.metric(
        "IBS + CBS bruto",
        moeda(ibs_cbs_bruto)
    )

    st.metric(
        "Créditos",
        moeda(creditos_ibs_cbs)
    )

    st.metric(
        "IBS + CBS líquido",
        moeda(ibs_cbs_liquido)
    )

with col3:
    st.subheader("Carga Total")

    st.metric(
        "Carga total estimada",
        moeda(carga_total)
    )


# ============================================================
# 11. ALÍQUOTAS DOS CINCO ANEXOS
# ============================================================

st.subheader("Alíquotas efetivas calculadas")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Anexo I", f"{a1:.2%}")

with col2:
    st.metric("Anexo II", f"{a2:.2%}")

with col3:
    st.metric("Anexo III", f"{a3:.2%}")

with col4:
    st.metric("Anexo IV", f"{a4:.2%}")

with col5:
    st.metric("Anexo V", f"{a5:.2%}")


# ============================================================
# 12. ALERTAS
# ============================================================

if anexo_selecionado == "Selecione o Anexo":
    st.warning(
        "Selecione o Anexo da empresa para concluir a simulação."
    )
elif receita_anual > 4_800_000:
    st.error(
        "A receita anual projetada ultrapassa R$ 4,8 milhões. "
        "O enquadramento no Simples Nacional deve ser analisado."
    )
elif receita_anual > 3_600_000:
    st.warning(
        "A receita anual projetada ultrapassa R$ 3,6 milhões. "
        "Verifique o tratamento específico aplicável ao ISS e IBS."
    )

if anexo_selecionado != "Selecione o Anexo":
    st.info(
        f"O cálculo principal do DAS está usando o {anexo_selecionado}, "
        f"correspondente à alíquota efetiva de {aliquota_selecionada:.2%}."
    )

st.caption(
    "Esta ferramenta é uma simulação gerencial e não substitui "
    "o cálculo oficial dos tributos nem a legislação vigente."
)
