document.addEventListener('DOMContentLoaded', () => {
  // Back to top
  const toTop = document.getElementById('backToTop');
  const toggleTop = () => { if(toTop) toTop.style.display = (window.scrollY > 400) ? 'inline-flex' : 'none'; };
  window.addEventListener('scroll', toggleTop); toggleTop();
  toTop?.addEventListener('click', () => window.scrollTo({top:0, behavior:'smooth'}));

  // Auto-init DataTables if present
  const $ = window.jQuery;
  const table = document.getElementById('otopTable');
  if (table && $ && $.fn.dataTable) {
    $(table).DataTable({
      pageLength: 10,
      lengthMenu: [10, 25, 50, 100],
      language: { url: "https://cdn.datatables.net/plug-ins/1.13.7/i18n/th.json" }
    });
  }
});
