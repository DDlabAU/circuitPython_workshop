function fetchData() {
    fetch('/api/data')
        .then(res => res.json())
        .then(data => {
            console.log(data);

            // update button count
            document.getElementById('button-count').textContent =
                data.button_count ?? '-';

            // update table row
            const r = data.reading;
            if (r) {
                document.getElementById('timestamp').textContent = r.timestamp ?? '-';
                document.getElementById('tvoc').textContent = r.tvoc ?? '-';
                document.getElementById('eco2').textContent = r.eco2 ?? '-';
            }
        })
        .catch(err => console.error(err));
}

// run immediately and every 2 seconds
fetchData();
setInterval(fetchData, 2000);