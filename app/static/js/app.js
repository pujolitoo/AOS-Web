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

  // Búsqueda de productos
  const inputSearch = document.getElementById('input-search');
  const btnSearch = document.getElementById('btn-search');

  function renderProducts(rows){
    const tbody = document.querySelector('.table-wrap tbody');
    if(!tbody) return;
    tbody.innerHTML = rows.map(p => {
      const precio = (typeof p.precio === 'number') ? p.precio.toFixed(2) : (p.precio || '0.00');
      return `\n              <tr>\n                <td data-label="ID">${p.id}</td>\n                <td data-label="Nombre">${p.nombre}</td>\n                <td data-label="Precio" class="price">${precio}</td>\n                <td data-label="Stock" class="stock">${p.stock}</td>\n                <td data-label="Acciones">\n                  <button class="btn-delete" data-id="${p.id}" style="background:#f87171;border:none;padding:6px 10px;border-radius:6px;color:#fff;cursor:pointer">Eliminar</button>\n                </td>\n              </tr>`;
    }).join('');
  }

  async function doSearch(q){
    try{
      let res;
      if(!q){
        res = await fetch('/productos');
        if(!res.ok) throw new Error('Error al obtener productos');
        const data = await res.json();
        renderProducts(data);
        return;
      }
      res = await fetch('/productos/buscar?nombre='+encodeURIComponent(q));
      const body = await res.json();
      // buscar devuelve {resultados: [], total: n} o {mensaje:..., resultados: []}
      const arr = body.resultados || [];
      renderProducts(arr);
    }catch(err){
      await showModal(String(err), {title:'Error', type:'error', confirm:false, okText:'Cerrar'});
    }
  }

  btnSearch?.addEventListener('click', ()=> doSearch(inputSearch.value.trim()));
  inputSearch?.addEventListener('keydown', (e)=>{ if(e.key === 'Enter'){ e.preventDefault(); doSearch(inputSearch.value.trim()); } });

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
