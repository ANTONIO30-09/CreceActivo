import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { guias } from './demo';
import './styles.css';

function App(){
 const [tab,setTab]=useState('Guías');
 const [query,setQuery]=useState('');
 const [edad,setEdad]=useState('Todas las edades');
 const [categoria,setCategoria]=useState('Todas');
 const [detalle,setDetalle]=useState(null);
 const [confirmacion,setConfirmacion]=useState(false);
 const visibles=guias.filter(g=>g.titulo.toLocaleLowerCase('es').includes(query.toLocaleLowerCase('es')) && (edad==='Todas las edades'||g.rango_edad===edad) && (categoria==='Todas'||g.categoria===categoria));
 return <div className="layout">
  <aside className="sidebar"><a className="brand" href="#" aria-label="CreceActivo, inicio">✳ <span>CreceActivo</span></a><p className="side-label">ESPACIO PARA FAMILIAS</p><nav aria-label="Módulo de nutrición">{['Guías','Menús','Orientación'].map((item,i)=><button key={item} className={tab===item?'nav-item active':'nav-item'} onClick={()=>{setTab(item);setDetalle(null);setConfirmacion(false);}}><span aria-hidden="true">{['▦','◒','♡'][i]}</span>{item}</button>)}</nav><div className="side-note"><span>Un paso a la vez.</span><p>Acompañamos el aprendizaje de hábitos en familia.</p></div><p className="side-footer">Módulo 02 · Nutrición</p></aside>
  <div className="content"><header className="topbar"><span>Nutrición y orientación profesional</span><span className="demo-badge">Vista de demostración</span></header>
  <main><div className="breadcrumb">CreceActivo / Nutrición / {tab}</div>
   <section className="hero"><div><span className="eyebrow">CRECER JUNTOS</span><h1>{tab==='Guías'?'Pequeños hábitos.\nGrandes comienzos.':tab==='Menús'?'Ideas para compartir\nen la mesa.':'Acompañamiento\npara tu familia.'}</h1><p>{tab==='Guías'?'Explora el espacio de guías de alimentación y hábitos familiares.':tab==='Menús'?'Un espacio para consultar menús y meriendas por edad.':'Prepara tu consulta para el equipo de profesionales.'}</p></div><div className="hero-art" aria-hidden="true"><div className="art-orbit"></div><span className="art-leaf">✳</span><span className="art-caption">Aprender · Compartir · Crecer</span></div></section>
   <div className="notice"><strong>Prototipo del módulo 2.</strong> Datos de ejemplo, pendientes de validación profesional. No hay conexión a la API ni envío de solicitudes.</div>
   {tab==='Guías' && <><div className="section-heading"><div><h2>Guías para tu familia</h2><p>Encuentra contenido por tema y rango de edad.</p></div><span>{visibles.length} resultados</span></div>
    <div className="filters"><label>Buscar guía<input type="search" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Escribe un título…"/></label><label>Rango de edad<select value={edad} onChange={e=>setEdad(e.target.value)}>{['Todas las edades','6-8 años','9-11 años','12-14 años'].map(e=><option key={e}>{e}</option>)}</select></label></div>
    <div className="chips" aria-label="Categorías">{['Todas','Hábitos','Meriendas','Alimentación'].map(c=><button aria-pressed={categoria===c} className={categoria===c?'selected':''} key={c} onClick={()=>setCategoria(c)}>{c}</button>)}</div>
    {detalle ? <section className="detail"><button className="text-button" onClick={()=>setDetalle(null)}>← Volver al catálogo</button><p className="eyebrow">{detalle.categoria} · {detalle.rango_edad}</p><h2>{detalle.titulo}</h2><p>{detalle.contenido}</p><h3>Hábitos clave</h3><ul>{detalle.habitos_clave.map(h=><li key={h}>{h}</li>)}</ul><span className="status">Pendiente de validación</span></section> : <div className="cards">{visibles.map(g=><article key={g.id} className="card"><div className={'card-art '+g.color}><span>{g.icono}</span><small>{g.categoria}</small></div><div className="card-body"><div className="card-meta"><span>{g.rango_edad}</span><span>Ejemplo</span></div><h3>{g.titulo}</h3><p>Contenido de muestra para revisar el diseño del catálogo.</p><button onClick={()=>setDetalle(g)} aria-label={'Ver guía: '+g.titulo}>Explorar guía <span aria-hidden="true">↗</span></button></div></article>)}</div>}
    {!detalle && visibles.length===0 && <div className="empty"><h3>No encontramos guías</h3><p>Prueba otro título o cambia los filtros.</p><button onClick={()=>{setQuery('');setEdad('Todas las edades');setCategoria('Todas');}}>Limpiar filtros</button></div>}
   </>}
   {tab==='Menús' && <section className="detail"><p className="eyebrow">PRÓXIMAMENTE</p><h2>Catálogo de menús y meriendas</h2><p>Esta sección está reservada para los menús revisados por nutricionistas. Se integrará con los campos de título, rango de edad, tipo de comida, platos y recomendaciones del módulo 2.</p><span className="status">Pendiente de contenido y conexión a la API</span></section>}
   {tab==='Orientación' && <section className="detail"><p className="eyebrow">SOLICITUD DE ORIENTACIÓN</p><h2>¿Sobre qué te gustaría conversar?</h2><p>Prueba el formulario con datos ficticios. No se guardan ni se envían.</p><form onSubmit={e=>{e.preventDefault();setConfirmacion(true);}} onChange={()=>setConfirmacion(false)}><label>Área de orientación<select required defaultValue=""><option value="" disabled>Selecciona un área</option><option>Nutrición</option><option>Pediatría</option><option>Actividad física</option></select></label><label>Tu consulta<textarea required minLength={10} maxLength={1000} placeholder="Describe una consulta de ejemplo (mínimo 10 caracteres)."/></label><button type="submit" className="primary">Probar solicitud</button></form>{confirmacion && <p role="status" className="success">Formulario validado en esta demostración. La solicitud no se ha enviado.</p>}</section>}
   <footer className="page-footer">CreceActivo · Educación y acompañamiento familiar.<br/>La plataforma no sustituye la consulta con un profesional de la salud.</footer>
  </main></div>
 </div>;
}
createRoot(document.getElementById('root')).render(<App/>);
