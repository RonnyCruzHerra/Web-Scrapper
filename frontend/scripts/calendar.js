document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');

  // Inicializa el calendario FullCalendar
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'es',
    events: async function (info, successCallback, failureCallback) {
      try {
        const res = await fetch('http://localhost:5000/api/scraped-data');
        const data = await res.json();

        console.log("Datos recibidos del backend:", data); // Debug

        // Filtra solo eventos con fecha válida
        const events = data
          .filter(entry => entry.scraped_at && !isNaN(new Date(entry.scraped_at).getTime()))
          .map(entry => ({
            title: entry.title || 'Dato scrapeado',
            start: entry.scraped_at,
            extendedProps: entry
          }));

        // Si no hay eventos válidos, muestra eventos de prueba
        if (events.length === 0) {
          console.warn("No se encontraron eventos con fecha válida, mostrando eventos de prueba");
          successCallback([
            { title: "Evento prueba 1", start: new Date().toISOString() },
            { title: "Evento prueba 2", start: "2025-07-25" }
          ]);
        } else {
          console.log("Eventos formateados para FullCalendar:", events);
          successCallback(events);
        }
      } catch (error) {
        console.error("Error cargando eventos:", error);
        failureCallback(error);
      }
    },
    eventClick: function (info) {
      const modal = document.getElementById('details-modal');
      const content = document.getElementById('event-details');
      const close = document.getElementById('close-modal');

      content.textContent = JSON.stringify(info.event.extendedProps, null, 2);
      modal.classList.remove('hidden');

      close.onclick = () => modal.classList.add('hidden');
    }
  });

  calendar.render();  // Renderiza el calendario una sola vez
  console.log("Calendario renderizado correctamente.");
});
