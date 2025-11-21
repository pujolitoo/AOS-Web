// JS para la interfaz de productos: formulario, modal y acciones CRUD
document.addEventListener('DOMContentLoaded', ()=>{
  const btnShow = document.getElementById('btn-show-form');
  const formWrap = document.getElementById('product-form');
  const btnCancel = document.getElementById('btn-cancel');
  const btnAdd = document.getElementById('btn-add');
  const formMsg = document.getElementById('form-msg');

  // Modal helpers
  const overlay = document.getElementById('modal-overlay');
  const modalBody = document.getElementById('modal-body');
  const modalOk = document.getElementById('modal-ok');
  const modalCancel = document.getElementById('modal-cancel');
  const modalClose = document.getElementById('modal-close');
  const modalTitle = document.getElementById('modal-title');
  const modalSub = document.getElementById('modal-sub');
  const modalIcon = document.getElementById('modal-icon');

  function setModalStyle(type){
  // type: 'info'|'error'|'confirm'
  if(type === 'error'){
    modalIcon.style.background = 'rgba(248,113,113,0.12)';
    modalIcon.style.color = '#b91c1c';
    modalOk.style.background = '#ef4444';
    modalOk.style.borderColor = 'transparent';
    modalBody.style.color = '#b91c1c';
  } else if(type === 'confirm'){
    modalIcon.style.background = 'rgba(245,158,11,0.12)';
    modalIcon.style.color = '#b45309';
    modalOk.style.background = '#f97316';
    modalBody.style.color = '#0f172a';
  } else { // info/default
    modalIcon.style.background = 'rgba(37,99,235,0.12)';
    modalIcon.style.color = 'var(--accent-2)';
    modalOk.style.background = 'var(--accent)';
    modalBody.style.color = '#0f172a';
  }
  }

  function showModal(message, {title='Mensaje', sub=null, type='info', confirm=false, okText='Aceptar', cancelText='Cancelar'}={}){
    return new Promise((resolve)=>{
      modalBody.textContent = message;
      modalTitle.textContent = title;
      modalSub.textContent = sub || '';
      modalOk.textContent = okText;
      modalCancel.textContent = cancelText;
      setModalStyle(type);
      if(confirm){ modalCancel.style.display = ''; } else { modalCancel.style.display = 'none'; }
      overlay.style.display = 'flex';
      // Handlers
      function cleanup(){ overlay.style.display='none'; modalOk.removeEventListener('click', onOk); modalCancel.removeEventListener('click', onCancel); modalClose.removeEventListener('click', onClose); }
      function onOk(){ cleanup(); resolve(true); }
      function onCancel(){ cleanup(); resolve(false); }
      function onClose(){ cleanup(); resolve(false); }
      modalOk.addEventListener('click', onOk);
      modalCancel.addEventListener('click', onCancel);
      modalClose.addEventListener('click', onClose);
    });
  }

  btnShow?.addEventListener('click', ()=>{
    formWrap.style.display = 'block';
    window.scrollTo({top: formWrap.offsetTop - 20, behavior: 'smooth'});
  });
  btnCancel?.addEventListener('click', ()=>{ formWrap.style.display = 'none'; formMsg.textContent = ''; });

  // Añadir producto via fetch
  btnAdd?.addEventListener('click', async ()=>{
    formMsg.textContent = '';
    const id = Number(document.getElementById('input-id').value);
    const nombre = document.getElementById('input-nombre').value.trim();
    const precio = Number(document.getElementById('input-precio').value);
    const stock = Number(document.getElementById('input-stock').value);
    if(!id || !nombre){ await showModal('ID y Nombre son requeridos', {title:'Error', type:'error', confirm:false, okText:'Cerrar'}); return; }
    const payload = { id, nombre, precio, stock };
    try{
      const res = await fetch('/productos', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
      const body = await res.json();
      if(res.ok){
        await showModal(body.mensaje || 'Creado correctamente', {title:'Éxito', type:'info', confirm:false, okText:'Cerrar'});
        setTimeout(()=> location.reload(), 400);
      } else {
        await showModal(body.detail || JSON.stringify(body), {title:'Error', type:'error', confirm:false, okText:'Cerrar'});
      }
    }catch(err){ await showModal(String(err), {title:'Error', type:'error', confirm:false, okText:'Cerrar'}); }
  });

  // Borrar producto (event delegation para soportar filas dinámicas)
  const tableWrap = document.querySelector('.table-wrap');
  if(tableWrap){
    tableWrap.addEventListener('click', async (e)=>{
      const btn = e.target.closest('.btn-delete');
      if(!btn) return;
      const id = btn.getAttribute('data-id');
      const ok = await showModal('¿Eliminar producto con ID '+id+'?', {title:'Confirmar eliminación', type:'confirm', confirm:true, okText:'Eliminar', cancelText:'Cancelar'});
      if(!ok) return;
      try{
        const res = await fetch('/productos/'+id, {method:'DELETE'});
        if(res.ok){
          // Quitar fila del DOM
          const row = btn.closest('tr'); if(row) row.remove();
          await showModal('Producto eliminado', {title:'Éxito', type:'info', confirm:false, okText:'Cerrar'});
        } else {
          const body = await res.json(); await showModal(body.detail || JSON.stringify(body), {title:'Error', type:'error', confirm:false, okText:'Cerrar'});
        }
      }catch(err){ await showModal(String(err), {title:'Error', type:'error', confirm:false, okText:'Cerrar'}); }
    });
  }
});
