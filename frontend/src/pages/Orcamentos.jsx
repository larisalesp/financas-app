import { useState, useEffect } from 'react'

const API = 'http://localhost:8000'

function Orcamentos() {
  const [status, setStatus] = useState([])
  const [valor, setValor] = useState('')
  const [resposta, setResposta] = useState(null)
  const token = localStorage.getItem('token')

  useEffect(() => {
    buscarStatus()
  }, [])

  async function buscarStatus() {
    const res = await fetch(`${API}/budgets/status`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    setStatus(data)
  }

  async function verificarGasto() {
    if (!valor) return
    const v = parseFloat(valor)
    const problemas = status.filter(b => b.disponivel < v)
    const ok = problemas.length === 0

    if (ok) {
      setResposta({ tipo: 'ok', mensagem: ` Sim! Você tem saldo disponível nos seus orçamentos.` })
    } else {
      const cats = problemas.map(p => p.categoria).join(', ')
      setResposta({ tipo: 'erro', mensagem: ` Cuidado! Esse gasto ultrapassa o limite de: ${cats}.` })
    }
  }

  function corBarra(percentual) {
    if (percentual >= 100) return '#B46A72'
    if (percentual >= 80) return '#e8a87c'
    return '#A8B58A'
  }

  return (
    <div style={{minHeight:'100vh', backgroundColor:'#FFF7E6'}}>

      {/* NAVBAR */}
      <div style={{backgroundColor:'#2D3A47', padding:'14px 20px', display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <span style={{color:'#F7C8D3', fontWeight:'700', fontSize:'1.1rem'}}>Flowly ꕥ</span>
        <button onClick={() => { localStorage.clear(); window.location.href='/' }} style={{background:'none', border:'none', color:'#A8B58A', cursor:'pointer'}}>
          sair
        </button>
      </div>

      <div style={{padding:'20px', maxWidth:'480px', margin:'0 auto'}}>

        {/* POSSO GASTAR ISSO */}
        <div style={{backgroundColor:'white', borderRadius:'16px', padding:'18px', marginBottom:'20px'}}>
          <div style={{fontSize:'0.9rem', fontWeight:'700', color:'#2D3A47', marginBottom:'4px'}}>
            Posso gastar isso? 
          </div>
          <div style={{fontSize:'0.72rem', color:'#A8B58A', marginBottom:'12px'}}>
            Digite um valor e veja se cabe no seu orçamento
          </div>
          <div style={{display:'flex', gap:'8px'}}>
            <input
              type="number"
              placeholder="R$ 0,00"
              value={valor}
              onChange={e => { setValor(e.target.value); setResposta(null) }}
              style={{flex:1, border:'1.5px solid #F7C8D3', borderRadius:'10px', padding:'8px 12px', fontSize:'0.85rem', outline:'none'}}
            />
            <button
              onClick={verificarGasto}
              style={{backgroundColor:'#B46A72', color:'white', border:'none', borderRadius:'10px', padding:'8px 16px', fontWeight:'600', cursor:'pointer', fontSize:'0.85rem'}}
            >
              Verificar
            </button>
          </div>
          {resposta && (
            <div style={{marginTop:'10px', padding:'10px 14px', borderRadius:'10px', fontSize:'0.78rem', fontWeight:'500',
              backgroundColor: resposta.tipo === 'ok' ? '#f0f7ed' : '#fdf0f0',
              color: resposta.tipo === 'ok' ? '#A8B58A' : '#B46A72'
            }}>
              {resposta.mensagem}
            </div>
          )}
        </div>

        {/* ORÇAMENTOS */}
        <div style={{fontSize:'0.85rem', fontWeight:'700', color:'#2D3A47', marginBottom:'12px'}}>
          Orçamentos do mês
        </div>

        {status.length === 0 && (
          <div style={{textAlign:'center', color:'#A8B58A', fontSize:'0.8rem', padding:'20px'}}>
            Nenhum orçamento criado ainda
          </div>
        )}

        {status.map((b, i) => (
          <div key={i} style={{backgroundColor:'white', borderRadius:'14px', padding:'14px 16px', marginBottom:'10px'}}>
            <div style={{display:'flex', justifyContent:'space-between', marginBottom:'8px'}}>
              <span style={{fontSize:'0.8rem', fontWeight:'600', color:'#2D3A47'}}>{b.categoria}</span>
              <span style={{fontSize:'0.72rem', color:'#A8B58A'}}>R$ {b.gasto.toFixed(2)} / R$ {b.limite.toFixed(2)}</span>
            </div>
            <div style={{height:'6px', backgroundColor:'#F7C8D3', borderRadius:'10px', overflow:'hidden'}}>
              <div style={{height:'100%', width:`${Math.min(b.percentual, 100)}%`, backgroundColor: corBarra(b.percentual), borderRadius:'10px', transition:'width 0.3s'}}></div>
            </div>
            <div style={{display:'flex', justifyContent:'space-between', marginTop:'5px'}}>
              <span style={{fontSize:'0.62rem', color:'#A8B58A'}}>{b.percentual}% usado</span>
              {b.alerta && (
                <span style={{fontSize:'0.62rem', color:'#B46A72', fontWeight:'600'}}>⚠️ Quase no limite!</span>
              )}
              {b.percentual >= 100 && (
                <span style={{fontSize:'0.62rem', color:'#B46A72', fontWeight:'600'}}>🔴 Limite atingido!</span>
              )}
            </div>
          </div>
        ))}

      </div>
    </div>
  )
}

export default Orcamentos