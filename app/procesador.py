import pandas as pd

def procesar_archivos(df_conexiones: pd.DataFrame, df_volumenes: pd.DataFrame) -> pd.DataFrame:
    """
    Para cada conexión inyectores-productores, busca los datos del inyector en df_volumenes,
    y genera un nuevo registro para cada fecha con los volúmenes distribuidos al productor
    según el DIST_BYPROD.
    """
    # Renomear colunas para garantir consistência
    df_conexiones = df_conexiones.rename(columns={"INJECTOR": "POZO INJECTOR"})

    resultados = []

    for _, row in df_conexiones.iterrows():
        pozo_inyector = row["POZO INJECTOR"]
        productor = row["PRODUCER"]
        fator = row["DIST_BYPROD"]

        # Seleciona linhas da tabela de volumes que correspondem ao injetor
        dados_inyector = df_volumenes[df_volumenes["POZO INJECTOR"] == pozo_inyector].copy()

        if dados_inyector.empty:
            continue

        # Multiplica os valores pelos fatores para gerar os dados do produtor
        dados_inyector["PRODUCER"] = productor
        dados_inyector["VOL_OIL_DIST"] = dados_inyector["Suma de VOL_OIL"].astype(float) * fator
        dados_inyector["VOL_WATER_DIST"] = dados_inyector["Suma de VOL_WATER"].astype(float) * fator
        dados_inyector["VOL_GAS_DIST"] = dados_inyector["Suma de VOL_GAS"].astype(float) * fator

        # Seleciona apenas colunas finais relevantes
        dados_resultado = dados_inyector[[
            "FECHA", "POZO INJECTOR", "PRODUCER",
            "VOL_OIL_DIST", "VOL_WATER_DIST", "VOL_GAS_DIST"
        ]].copy()

        resultados.append(dados_resultado)

    # Concatena os resultados finais
    df_resultado = pd.concat(resultados, ignore_index=True)
    return df_resultado
