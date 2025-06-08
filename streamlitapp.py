<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Media Intelligence Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Inter Font -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <!-- Plotly.js CDN -->
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    <!-- html2canvas and jsPDF for PDF export -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #F0F8FF; /* Alice Blue - very light pastel blue */
            color: #333;
        }
        .pastel-blue-bg {
            background-color: #B3E0FF; /* Light Sky Blue */
        }
        .soft-blue-text {
            color: #8CD6FF; /* Cornflower Blue */
        }
        .accent-blue-bg {
            background-color: #A8DADC; /* Light Teal */
        }
        .filter-input {
            @apply p-2 rounded-lg border border-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-300;
        }
        .chart-container {
            @apply bg-white p-6 rounded-xl shadow-lg transition-all duration-300 hover:shadow-xl flex flex-col;
        }
        .insights-box {
            @apply mt-4 p-4 bg-blue-50 rounded-lg text-sm text-blue-800;
        }
        /* Custom modal styles */
        .modal {
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1000; /* Sit on top */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background-color: #fefefe;
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            width: 80%; /* Could be adjusted */
            max-width: 500px;
            text-align: center;
        }
        .modal-close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        .modal-close:hover,
        .modal-close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
    </style>
</head>
<body class="flex flex-col min-h-screen">
    <!-- Header -->
    <header class="bg-gradient-to-r from-blue-300 to-blue-500 text-white p-4 shadow-md rounded-b-xl flex justify-between items-center">
        <h1 class="text-3xl font-bold">Interactive Media Intelligence Dashboard</h1>
        <button id="exportPdfBtn" class="bg-blue-700 hover:bg-blue-800 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition-all duration-300">
            Ekspor Dashboard ke PDF
        </button>
    </header>

    <!-- Main Content Area -->
    <div class="flex flex-1 p-6 space-x-6" id="dashboard-content">
        <!-- Input and Filter Sidebar -->
        <aside class="w-1/4 bg-white p-6 rounded-xl shadow-lg flex flex-col space-y-6">
            <h2 class="text-2xl font-semibold text-soft-blue-text mb-4">Masukan Data</h2>

            <!-- CSV Upload Section -->
            <div>
                <label for="csvFileInput" class="block text-gray-700 font-medium mb-2">Unggah File CSV</label>
                <input type="file" id="csvFileInput" accept=".csv" class="filter-input w-full">
                <button id="loadCsvBtn" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md transition-all duration-300 mt-3 w-full">
                    Muat Data dari CSV
                </button>
                <p class="text-sm text-gray-500 mt-2">Pastikan CSV memiliki kolom: Date, Platform, Sentiment, MediaType, Location, Engagements.</p>
            </div>

            <hr class="border-t-2 border-blue-100 my-6">

            <h2 class="text-2xl font-semibold text-soft-blue-text mb-4">Filter Data</h2>

            <!-- Platform Filter -->
            <div>
                <label for="platformFilter" class="block text-gray-700 font-medium mb-2">Platform</label>
                <select id="platformFilter" class="filter-input w-full">
                    <option value="">Semua Platform</option>
                </select>
            </div>

            <!-- Sentiment Filter -->
            <div>
                <label for="sentimentFilter" class="block text-gray-700 font-medium mb-2">Sentimen</label>
                <select id="sentimentFilter" class="filter-input w-full">
                    <option value="">Semua Sentimen</option>
                    <option value="Positive">Positif</option>
                    <option value="Neutral">Netral</option>
                    <option value="Negative">Negatif</option>
                </select>
            </div>

            <!-- Media Type Filter -->
            <div>
                <label for="mediaTypeFilter" class="block text-gray-700 font-medium mb-2">Tipe Media</label>
                <select id="mediaTypeFilter" class="filter-input w-full">
                    <option value="">Semua Tipe Media</option>
                </select>
            </div>

            <!-- Location Filter -->
            <div>
                <label for="locationFilter" class="block text-gray-700 font-medium mb-2">Lokasi</label>
                <select id="locationFilter" class="filter-input w-full">
                    <option value="">Semua Lokasi</option>
                </select>
            </div>

            <!-- Date Range Filter -->
            <div>
                <label for="startDateFilter" class="block text-gray-700 font-medium mb-2">Rentang Tanggal (Mulai)</label>
                <input type="date" id="startDateFilter" class="filter-input w-full mb-4">

                <label for="endDateFilter" class="block text-gray-700 font-medium mb-2">Rentang Tanggal (Selesai)</label>
                <input type="date" id="endDateFilter" class="filter-input w-full">
            </div>

            <button id="applyFiltersBtn" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-4 rounded-lg shadow-md transition-all duration-300">
                Terapkan Filter
            </button>
        </aside>

        <!-- Charts Area -->
        <main class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-6 auto-rows-min">
            <h2 class="text-2xl font-semibold text-soft-blue-text md:col-span-2 mb-4">Visualisasi Data & Insights</h2>

            <!-- Placeholder message if no data loaded -->
            <div id="noDataMessage" class="md:col-span-2 text-center text-gray-600 p-8 bg-white rounded-xl shadow-lg">
                <p class="text-xl">Silakan unggah file CSV Anda untuk melihat visualisasi data.</p>
                <p class="text-md mt-2">Pastikan file CSV memiliki kolom: `Date`, `Platform`, `Sentiment`, `MediaType`, `Location`, `Engagements`.</p>
            </div>

            <!-- Sentiment Breakdown -->
            <div class="chart-container hidden" id="sentimentChartContainer">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">Sentiment Breakdown</h3>
                <div id="sentimentChart" class="flex-1 min-h-[300px]"></div>
                <div class="insights-box">
                    <p class="font-bold">Insight:</p>
                    <ul class="list-disc list-inside">
                        <li>Mayoritas sentimen positif menunjukkan citra merek yang kuat.</li>
                        <li>Persentase sentimen netral yang signifikan mengindikasikan peluang untuk mengubah audiens yang ragu-ragu.</li>
                        <li>Perhatikan sentimen negatif; peningkatan tiba-tiba bisa menjadi sinyal masalah.</li>
                    </ul>
                </div>
            </div>

            <!-- Platform Engagements -->
            <div class="chart-container hidden" id="platformChartContainer">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">Platform Engagements</h3>
                <div id="platformChart" class="flex-1 min-h-[300px]"></div>
                <div class="insights-box">
                    <p class="font-bold">Insight:</p>
                    <ul class="list-disc list-inside">
                        <li>Platform dengan engagement tertinggi adalah saluran utama interaksi audiens Anda.</li>
                        <li>Platform dengan engagement rendah mungkin memerlukan evaluasi ulang strategi konten atau penargetan audiens.</li>
                        <li>Konten tertentu mungkin berkinerja lebih baik di platform spesifik, sesuaikan strategi Anda.</li>
                    </ul>
                </div>
            </div>

            <!-- Engagement Trend over Time -->
            <div class="chart-container md:col-span-2 hidden" id="engagementTrendChartContainer">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">Engagement Trend over Time</h3>
                <div id="engagementTrendChart" class="flex-1 min-h-[350px]"></div>
                <div class="insights-box">
                    <p class="font-bold">Insight:</p>
                    <ul class="list-disc list-inside">
                        <li>Lonjakan engagement setelah peluncuran kampanye menandakan keberhasilan.</li>
                        <li>Engagement cenderung memuncak dalam 24-48 jam pertama setelah publikasi konten.</li>
                        <li>Identifikasi tren musiman untuk merencanakan konten yang relevan.</li>
                    </ul>
                </div>
            </div>

            <!-- Media Type Mix -->
            <div class="chart-container hidden" id="mediaTypeChartContainer">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">Media Type Mix</h3>
                <div id="mediaTypeChart" class="flex-1 min-h-[300px]"></div>
                <div class="insights-box">
                    <p class="font-bold">Insight:</p>
                    <ul class="list-disc list-inside">
                        <li>Tipe media dominan mencerminkan preferensi audiens Anda.</li>
                        <li>Jika artikel memiliki engagement tinggi tetapi proporsinya rendah, pertimbangkan untuk membuat lebih banyak.</li>
                        <li>Diversifikasi tipe media dapat membantu menjangkau audiens yang lebih luas.</li>
                    </ul>
                </div>
            </div>

            <!-- Top 5 Locations by Engagement -->
            <div class="chart-container hidden" id="locationChartContainer">
                <h3 class="text-xl font-semibold text-gray-800 mb-2">Top 5 Locations by Engagement</h3>
                <div id="locationChart" class="flex-1 min-h-[300px]"></div>
                <div class="insights-box">
                    <p class="font-bold">Insight:</p>
                    <ul class="list-disc list-inside">
                        <li>Lokasi teratas adalah area dengan minat tinggi terhadap merek/topik Anda.</li>
                        <li>Data ini mendukung kampanye pemasaran atau konten yang dilokalisasi.</li>
                        <li>Area di luar 5 besar dengan engagement yang muncul bisa menjadi target ekspansi.</li>
                    </ul>
                </div>
            </div>
        </main>
    </div>

    <!-- Custom Message Box Modal -->
    <div id="messageModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" id="closeMessageModal">&times;</span>
            <p id="modalMessage" class="text-lg font-semibold text-gray-800"></p>
        </div>
    </div>

    <script>
        let rawData = []; // Raw data from CSV
        let cleanedData = []; // Cleaned and processed data
        const pastelColors = ['#8CD6FF', '#B3E0FF', '#A8DADC', '#C7E9FB', '#6DBAE7']; // Color palette

        // --- Helper Functions ---

        /**
         * Displays a custom modal message.
         * @param {string} message - The message to display.
         */
        function showMessage(message) {
            document.getElementById('modalMessage').textContent = message;
            document.getElementById('messageModal').style.display = 'flex';
        }

        /**
         * Hides the custom modal message.
         */
        function hideMessage() {
            document.getElementById('messageModal').style.display = 'none';
        }

        /**
         * Parses CSV text into an array of objects.
         * Assumes the first row is the header.
         * @param {string} csvText - The raw CSV string.
         * @returns {Array<Object>} An array of objects representing CSV rows.
         */
        function parseCSV(csvText) {
            const lines = csvText.split('\n').filter(line => line.trim() !== '');
            if (lines.length === 0) return [];

            const headers = lines[0].split(',').map(header => header.trim());
            const dataRows = lines.slice(1);

            return dataRows.map(row => {
                const values = row.split(',').map(value => value.trim());
                const obj = {};
                headers.forEach((header, index) => {
                    // Convert numeric values to numbers if possible
                    if (header === 'Engagements') {
                        obj[header] = values[index] === '' ? null : Number(values[index]);
                    } else {
                        obj[header] = values[index];
                    }
                });
                return obj;
            });
        }

        /**
         * 2. Data Cleaning:
         * - Converts 'Date' string to Date objects.
         * - Fills empty or invalid 'Engagements' with 0.
         * @param {Array<Object>} data - The raw data array.
         * @returns {Array<Object>} The cleaned data array.
         */
        function cleanData(data) {
            return data.map(item => ({
                ...item,
                Date: new Date(item.Date), // Convert to datetime object
                Engagements: item.Engagements === null || isNaN(item.Engagements) ? 0 : Number(item.Engagements) // Fill empty/invalid engagements with 0
            }));
        }

        /**
         * Populates filter dropdowns with unique values from the cleaned data.
         */
        function populateFilterOptions() {
            const platforms = new Set();
            const mediaTypes = new Set();
            const locations = new Set();

            cleanedData.forEach(item => {
                platforms.add(item.Platform);
                mediaTypes.add(item.MediaType);
                locations.add(item.Location);
            });

            const populateSelect = (selectId, optionsSet) => {
                const selectElement = document.getElementById(selectId);
                // Clear existing options, keep "Semua..."
                const defaultOption = selectElement.querySelector('option[value=""]');
                selectElement.innerHTML = '';
                // Re-add default option if it exists, otherwise create it
                if (defaultOption) {
                    selectElement.appendChild(defaultOption);
                } else {
                    const opt = document.createElement('option');
                    opt.value = "";
                    opt.textContent = "Semua " + selectId.replace('Filter', '').replace(/([A-Z])/g, ' $1').trim(); // "Semua Platform", "Semua Tipe Media" etc.
                    selectElement.appendChild(opt);
                }


                Array.from(optionsSet).sort().forEach(option => {
                    const opt = document.createElement('option');
                    opt.value = option;
                    opt.textContent = option;
                    selectElement.appendChild(opt);
                });
            };

            populateSelect('platformFilter', platforms);
            populateSelect('mediaTypeFilter', mediaTypes);
            populateSelect('locationFilter', locations);
        }

        /**
         * Renders all Plotly charts based on the filtered data.
         * 3. Visualisasi (Plotly)
         * - Pie Chart: Sentiment Breakdown
         * - Line Chart: Engagement Trend over Time
         * - Bar Chart: Platform Engagements
         * - Pie Chart: Media Type Mix
         * - Bar Chart: Top 5 Locations
         * @param {Array<Object>} data - The filtered data to visualize.
         */
        function renderCharts(data) {
            // Hide message, show containers
            document.getElementById('noDataMessage').classList.add('hidden');
            document.getElementById('sentimentChartContainer').classList.remove('hidden');
            document.getElementById('platformChartContainer').classList.remove('hidden');
            document.getElementById('engagementTrendChartContainer').classList.remove('hidden');
            document.getElementById('mediaTypeChartContainer').classList.remove('hidden');
            document.getElementById('locationChartContainer').classList.remove('hidden');

            // --- Sentiment Breakdown ---
            const sentimentCounts = data.reduce((acc, item) => {
                acc[item.Sentiment] = (acc[item.Sentiment] || 0) + 1;
                return acc;
            }, {});
            const sentimentLabels = Object.keys(sentimentCounts);
            const sentimentValues = Object.values(sentimentCounts);

            const sentimentData = [{
                labels: sentimentLabels,
                values: sentimentValues,
                type: 'pie',
                marker: { colors: pastelColors.slice(0, sentimentLabels.length) },
                hoverinfo: 'label+percent',
                textinfo: 'percent',
                hole: .4
            }];
            const sentimentLayout = {
                margin: {t: 0, b: 0, l: 0, r: 0}, showlegend: true,
                legend: { x: 0.1, y: 1.1, orientation: "h", font: { family: 'Inter', size: 12, color: '#333' } },
                font: { family: 'Inter', size: 12, color: '#333' }
            };
            Plotly.newPlot('sentimentChart', sentimentData, sentimentLayout, {responsive: true, displayModeBar: false});

            // --- Engagement Trend over Time ---
            const engagementTrend = data.reduce((acc, item) => {
                const dateString = item.Date.toISOString().split('T')[0];
                if (!acc[dateString]) {
                    acc[dateString] = 0;
                }
                acc[dateString] += item.Engagements;
                return acc;
            }, {});
            const sortedDates = Object.keys(engagementTrend).sort();
            const trendValues = sortedDates.map(date => engagementTrend[date]);

            const trendData = [{
                x: sortedDates, y: trendValues, mode: 'lines+markers',
                marker: { color: pastelColors[0] }, line: { color: pastelColors[1], width: 3 }
            }];
            const trendLayout = {
                xaxis: { title: 'Tanggal', showgrid: false, tickfont: { family: 'Inter', size: 10 } },
                yaxis: { title: 'Engagement', showgrid: true, gridcolor: '#e0e0e0', tickfont: { family: 'Inter', size: 10 } },
                margin: { t: 20, r: 20, b: 60, l: 60 }, hovermode: 'x unified',
                font: { family: 'Inter', size: 12, color: '#333' }
            };
            Plotly.newPlot('engagementTrendChart', trendData, trendLayout, {responsive: true, displayModeBar: false});

            // --- Platform Engagements ---
            const platformCounts = data.reduce((acc, item) => {
                acc[item.Platform] = (acc[item.Platform] || 0) + item.Engagements;
                return acc;
            }, {});
            const platformLabels = Object.keys(platformCounts);
            const platformValues = Object.values(platformCounts);

            const platformData = [{
                x: platformLabels, y: platformValues, type: 'bar',
                marker: { color: platformLabels.map((_, i) => pastelColors[i % pastelColors.length]) }
            }];
            const platformLayout = {
                xaxis: { title: 'Platform', showgrid: false, tickfont: { family: 'Inter', size: 10 } },
                yaxis: { title: 'Total Engagement', showgrid: true, gridcolor: '#e0e0e0', tickfont: { family: 'Inter', size: 10 } },
                margin: { t: 20, r: 20, b: 60, l: 60 },
                font: { family: 'Inter', size: 12, color: '#333' }
            };
            Plotly.newPlot('platformChart', platformData, platformLayout, {responsive: true, displayModeBar: false});

            // --- Media Type Mix ---
            const mediaTypeCounts = data.reduce((acc, item) => {
                acc[item.MediaType] = (acc[item.MediaType] || 0) + 1;
                return acc;
            }, {});
            const mediaTypeLabels = Object.keys(mediaTypeCounts);
            const mediaTypeValues = Object.values(mediaTypeCounts);

            const mediaTypeData = [{
                labels: mediaTypeLabels, values: mediaTypeValues, type: 'pie',
                marker: { colors: pastelColors.slice(0, mediaTypeLabels.length) },
                hoverinfo: 'label+percent', textinfo: 'percent', hole: .4
            }];
            const mediaTypeLayout = {
                margin: {t: 0, b: 0, l: 0, r: 0}, showlegend: true,
                legend: { x: 0.1, y: 1.1, orientation: "h", font: { family: 'Inter', size: 12, color: '#333' } },
                font: { family: 'Inter', size: 12, color: '#333' }
            };
            Plotly.newPlot('mediaTypeChart', mediaTypeData, mediaTypeLayout, {responsive: true, displayModeBar: false});

            // --- Top 5 Locations by Engagement ---
            const locationEngagements = data.reduce((acc, item) => {
                acc[item.Location] = (acc[item.Location] || 0) + item.Engagements;
                return acc;
            }, {});
            const sortedLocations = Object.entries(locationEngagements)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 5);

            const locationLabels = sortedLocations.map(item => item[0]);
            const locationValues = sortedLocations.map(item => item[1]);

            const locationData = [{
                x: locationLabels, y: locationValues, type: 'bar',
                marker: { color: locationLabels.map((_, i) => pastelColors[i % pastelColors.length]) }
            }];
            const locationLayout = {
                xaxis: { title: 'Lokasi', showgrid: false, tickfont: { family: 'Inter', size: 10 } },
                yaxis: { title: 'Total Engagement', showgrid: true, gridcolor: '#e0e0e0', tickfont: { family: 'Inter', size: 10 } },
                margin: { t: 20, r: 20, b: 60, l: 60 },
                font: { family: 'Inter', size: 12, color: '#333' }
            };
            Plotly.newPlot('locationChart', locationData, locationLayout, {responsive: true, displayModeBar: false});
        }

        /**
         * 4. Filter data:
         * - Platform
         * - Sentiment
         * - Media Type
         * - Location
         * - Rentang Tanggal
         * Applies filters to the data and re-renders charts.
         */
        function applyFilters() {
            if (cleanedData.length === 0) {
                // If no data is loaded, show the initial message and hide charts
                document.getElementById('noDataMessage').classList.remove('hidden');
                document.getElementById('sentimentChartContainer').classList.add('hidden');
                document.getElementById('platformChartContainer').classList.add('hidden');
                document.getElementById('engagementTrendChartContainer').classList.add('hidden');
                document.getElementById('mediaTypeChartContainer').classList.add('hidden');
                document.getElementById('locationChartContainer').classList.add('hidden');
                return;
            }

            const platform = document.getElementById('platformFilter').value;
            const sentiment = document.getElementById('sentimentFilter').value;
            const mediaType = document.getElementById('mediaTypeFilter').value;
            const location = document.getElementById('locationFilter').value;
            const startDate = document.getElementById('startDateFilter').value ? new Date(document.getElementById('startDateFilter').value) : null;
            const endDate = document.getElementById('endDateFilter').value ? new Date(document.getElementById('endDateFilter').value) : null;

            let filtered = cleanedData;

            if (platform) {
                filtered = filtered.filter(item => item.Platform === platform);
            }
            if (sentiment) {
                filtered = filtered.filter(item => item.Sentiment === sentiment);
            }
            if (mediaType) {
                filtered = filtered.filter(item => item.MediaType === mediaType);
            }
            if (location) {
                filtered = filtered.filter(item => item.Location === location);
            }
            if (startDate) {
                filtered = filtered.filter(item => item.Date >= startDate);
            }
            if (endDate) {
                // Add one day to endDate to include the whole day
                const adjustedEndDate = new Date(endDate);
                adjustedEndDate.setDate(adjustedEndDate.getDate() + 1);
                filtered = filtered.filter(item => item.Date < adjustedEndDate);
            }

            renderCharts(filtered);
        }

        /**
         * 5. Fitur ekspor PDF seluruh dashboard.
         * Exports the entire dashboard content as a PDF.
         */
        async function exportPdf() {
            const exportBtn = document.getElementById('exportPdfBtn');
            const originalBtnText = exportBtn.textContent;
            exportBtn.textContent = 'Mengekspor...';
            exportBtn.disabled = true;

            const dashboard = document.getElementById('dashboard-content');
            try {
                // Temporarily hide filter sidebar to get full dashboard width for PDF
                const sidebar = document.querySelector('aside');
                sidebar.style.display = 'none';
                const mainContent = document.querySelector('main');
                mainContent.style.width = '100%'; // Make main content fill space

                // Ensure all charts are rendered before capturing
                await new Promise(resolve => setTimeout(resolve, 500)); // Small delay for rendering

                const canvas = await html2canvas(dashboard, {
                    scale: 2,
                    useCORS: true,
                    logging: false,
                    allowTaint: true,
                    scrollY: -window.scrollY
                });

                // Restore sidebar and main content width
                sidebar.style.display = 'flex';
                mainContent.style.width = ''; // Reset to auto

                const imgData = canvas.toDataURL('image/png');
                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF('p', 'mm', 'a4');

                const imgWidth = 210;
                const pageHeight = 297;
                const imgHeight = canvas.height * imgWidth / canvas.width;
                let heightLeft = imgHeight;
                let position = 0;

                pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;

                while (heightLeft >= 0) {
                    position = heightLeft - imgHeight;
                    pdf.addPage();
                    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                    heightLeft -= pageHeight;
                }

                pdf.save('Interactive_Media_Intelligence_Dashboard.pdf');
                showMessage("Dashboard berhasil diekspor ke PDF!");
            } catch (error) {
                console.error("Error generating PDF:", error);
                showMessage("Gagal mengekspor PDF. Pastikan semua elemen dimuat dengan benar dan coba lagi.");
            } finally {
                exportBtn.textContent = originalBtnText;
                exportBtn.disabled = false;
            }
        }


        // --- Event Listeners ---
        document.addEventListener('DOMContentLoaded', () => {
            // Initial render (will show placeholder message)
            applyFilters();

            // Load CSV Button
            document.getElementById('loadCsvBtn').addEventListener('click', () => {
                const fileInput = document.getElementById('csvFileInput');
                const file = fileInput.files[0];

                if (!file) {
                    showMessage("Mohon pilih file CSV terlebih dahulu.");
                    return;
                }

                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        rawData = parseCSV(e.target.result);
                        if (rawData.length === 0) {
                            showMessage("File CSV kosong atau tidak valid.");
                            return;
                        }
                        cleanedData = cleanData(rawData);
                        populateFilterOptions();
                        applyFilters(); // Render charts with new data
                        showMessage("Data CSV berhasil dimuat dan visualisasi diperbarui!");
                    } catch (error) {
                        console.error("Error processing CSV:", error);
                        showMessage("Terjadi kesalahan saat memproses file CSV. Pastikan formatnya benar.");
                    }
                };
                reader.readAsText(file);
            });

            // Filter button and change events
            document.getElementById('applyFiltersBtn').addEventListener('click', applyFilters);
            document.getElementById('platformFilter').addEventListener('change', applyFilters);
            document.getElementById('sentimentFilter').addEventListener('change', applyFilters);
            document.getElementById('mediaTypeFilter').addEventListener('change', applyFilters);
            document.getElementById('locationFilter').addEventListener('change', applyFilters);
            document.getElementById('startDateFilter').addEventListener('change', applyFilters);
            document.getElementById('endDateFilter').addEventListener('change', applyFilters);

            // PDF Export button
            document.getElementById('exportPdfBtn').addEventListener('click', exportPdf);

            // Modal close button
            document.getElementById('closeMessageModal').addEventListener('click', hideMessage);
            window.addEventListener('click', (event) => {
                if (event.target == document.getElementById('messageModal')) {
                    hideMessage();
                }
            });

            // Adjust chart sizes on window resize for responsiveness
            window.addEventListener('resize', () => {
                applyFilters(); // Re-render charts with current filtered data to adjust sizes
            });
        });
    </script>
</body>
</html>
