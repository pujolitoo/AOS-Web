// JS para la interfaz de productos: formulario, modal y acciones CRUD
// API_BASE_URL se configura dinámicamente para apuntar al servicio backend
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://localhost:8000'  // Desarrollo local
  : 'http://api:8000';        // Docker compose (desde el navegador no funcionará, se debe usar proxy o mismo host)

// Para docker-compose, el frontend proxy las peticiones o usamos el mismo puerto
// Por simplicidad, usaremos rutas relativas que el navegador resolverá contra el puerto actual
// y agregaremos un proxy en el frontend si es necesario.
// Por ahora, asumiremos que el API está en el mismo host pero diferente puerto para desarrollo.
const API_URL = '/api'; // El frontend hará proxy de /api -> api:8000

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

  // Añadir/Actualizar producto via fetch (soporta modo edición)
  btnAdd?.addEventListener('click', async ()=>{
    formMsg.textContent = '';
    const editingIdEl = document.getElementById('editing-id');
    const editing = editingIdEl ? editingIdEl.value : '';
    const id = Number(document.getElementById('input-id').value);
    const nombre = document.getElementById('input-nombre').value.trim();
    const precio = Number(document.getElementById('input-precio').value);
    const stock = Number(document.getElementById('input-stock').value);
    if(!id || !nombre){ await showModal('ID y Nombre son requeridos', {title:'Error', type:'error', confirm:false, okText:'Cerrar'}); return; }
    const payload = { id, nombre, precio, stock };
    try{
      if(editing){
        // Edit mode -> PUT
        const res = await fetch(API_URL + '/productos/'+editing, {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
        const body = await res.json();
        if(res.ok){
          await showModal(body.mensaje || 'Actualizado correctamente', {title:'Éxito', type:'info', confirm:false, okText:'Cerrar'});
          // Reset form editing state
          editingIdEl.value = '';
          document.getElementById('input-id').disabled = false;
          document.getElementById('form-title').textContent = 'Añadir nuevo producto';
          document.getElementById('btn-add').textContent = 'Guardar';
          setTimeout(()=> doSearch(inputSearch.value.trim()), 200);
        } else {
          await showModal(body.detail || JSON.stringify(body), {title:'Error', type:'error', confirm:false, okText:'Cerrar'});
        }
      } else {
        // Create
        const res = await fetch(API_URL + '/productos', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
        const body = await res.json();
        if(res.ok){
          await showModal(body.mensaje || 'Creado correctamente', {title:'Éxito', type:'info', confirm:false, okText:'Cerrar'});
          setTimeout(()=> doSearch(inputSearch.value.trim()), 200);
        } else {
          await showModal(body.detail || JSON.stringify(body), {title:'Error', type:'error', confirm:false, okText:'Cerrar'});
        }
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
      return `\n              <tr>\n                <td data-label="ID">${p.id}</td>\n                <td data-label="Nombre">${p.nombre}</td>\n                <td data-label="Precio" class="price">${precio}</td>\n                <td data-label="Stock" class="stock">${p.stock}</td>\n                <td data-label="Acciones">\n                  <button class="btn-edit" data-id="${p.id}" style="background:#60a5fa;border:none;padding:6px 10px;border-radius:6px;color:#fff;cursor:pointer;margin-right:6px">Editar</button>\n                  <button class="btn-delete" data-id="${p.id}" style="background:#f87171;border:none;padding:6px 10px;border-radius:6px;color:#fff;cursor:pointer">Eliminar</button>\n                </td>\n              </tr>`;
    }).join('');
  }

  async function doSearch(q){
    try{
      let res;
      if(!q){
        res = await fetch(API_URL + '/productos');
        if(!res.ok) throw new Error('Error al obtener productos');
        const data = await res.json();
        renderProducts(data);
        return;
      }
      res = await fetch(API_URL + '/productos/buscar?nombre='+encodeURIComponent(q));
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

  // Borrar / Editar producto (event delegation para soportar filas dinámicas)
  const tableWrap = document.querySelector('.table-wrap');
  if(tableWrap){
    tableWrap.addEventListener('click', async (e)=>{
      // Edit action
      const btnEdit = e.target.closest('.btn-edit');
      if(btnEdit){
        const id = btnEdit.getAttribute('data-id');
        try{
          const res = await fetch(API_URL + '/productos/'+id);
          if(!res.ok) throw new Error('No se pudo obtener el producto');
          const p = await res.json();
          // Prefill form
          document.getElementById('input-id').value = p.id;
          document.getElementById('input-nombre').value = p.nombre;
          document.getElementById('input-precio').value = p.precio;
          document.getElementById('input-stock').value = p.stock;
          document.getElementById('editing-id').value = p.id;
          document.getElementById('form-title').textContent = 'Editar producto';
          document.getElementById('input-id').disabled = true;
          document.getElementById('btn-add').textContent = 'Guardar cambios';
          const formWrap = document.getElementById('product-form'); formWrap.style.display = 'block';
          window.scrollTo({top: formWrap.offsetTop - 20, behavior: 'smooth'});
        }catch(err){ await showModal(String(err), {title:'Error', type:'error', confirm:false, okText:'Cerrar'}); }
        return;
      }

      // Delete action
      const btn = e.target.closest('.btn-delete');
      if(!btn) return;
      const id = btn.getAttribute('data-id');
      const ok = await showModal('¿Eliminar producto con ID '+id+'?', {title:'Confirmar eliminación', type:'confirm', confirm:true, okText:'Eliminar', cancelText:'Cancelar'});
      if(!ok) return;
      try{
        const res = await fetch(API_URL + '/productos/'+id, {method:'DELETE'});
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

  // Clean editing state when cancelling
  btnCancel?.addEventListener('click', ()=>{
    const editing = document.getElementById('editing-id'); if(editing) editing.value = '';
    document.getElementById('form-title').textContent = 'Añadir nuevo producto';
    document.getElementById('input-id').disabled = false;
    document.getElementById('btn-add').textContent = 'Guardar';
    formWrap.style.display = 'none'; formMsg.textContent = '';
  });
});
