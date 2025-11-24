import json

# JSON retornado pela API
response_json = '{"response":"🔥 IDEIA 1 — "3 Sinais de Que Você Precisa Trocar de Pediatra AGORA"\\nÂngulo: alerta + autoridade médica\\nTese: A maioria dos pais ignora sinais sutis que indicam que o pediatra pode estar desatualizado ou errando no cuidado do seu filho.\\nPolêmica: "Se você já ouviu uma dessas frases na consulta, cuidado: seu filho pode estar em risco."\\n\\n🔥 IDEIA 2 — "A Verdade Chocante Sobre Antibióticos em Crianças"\\nÂngulo: quebrando crenças + educação\\nTese: O uso incorreto de antibióticos pode fazer mais mal do que bem — e poucos médicos explicam o verdadeiro perigo por trás de uma receita \'por precaução\'.\\nPolêmica: "Dar antibiótico sem necessidade pode sabotar a saúde futura do seu filho."\\n\\n🔥 IDEIA 3 — "O Maior Erro de Pais em Consultas Pediátricas"\\nÂngulo: identificação + solução prática\\nTese: Muitos pais não contam determinados sintomas por vergonha ou medo e isso pode atrasar diagnósticos importantes.\\nPolêmica: "Seu silêncio pode ser um inimigo oculto na saúde do seu filho.","session_id":"thread_oTdL1Anyw8OdPKblHf0z516v"}'

try:
    parsed = json.loads(response_json)
    print("✅ JSON é VÁLIDO!")
    print("\nConteúdo parseado:")
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
except json.JSONDecodeError as e:
    print(f"❌ JSON INVÁLIDO: {e}")
