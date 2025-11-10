document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('inputForm');
    const tableContainer = document.getElementById('tableContainer');
    const xInput = document.getElementById('xMax');
    const nInput = document.getElementById('nMax');
    const ctx = document.getElementById('functionChart').getContext('2d');
    let functionChart; // переменная для объекта Chart.js для удаления/обновления графика

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        xInput.style.borderColor = '';
        nInput.style.borderColor = '';

        const xMax = parseFloat(xInput.value);
        const nMax = parseInt(nInput.value);

        let hasError = false;

        if (isNaN(xMax) || xMax < -1 || xMax > 1) {
            alert('Введите x в диапазоне [-1, 1]');
            xInput.style.borderColor = 'red';
            hasError = true;
        }

        if (isNaN(nMax) || nMax <= 0) {
            alert('Введите целое n > 0');
            nInput.style.borderColor = 'red';
            hasError = true;
        }

        if (hasError) return;

        const steps = 50; // кол-во точек на графике
        const xValues = [];
        const fSeries = [];
        const fExact = [];

        for (let i = 0; i <= steps; i++) {
            const x = parseFloat(((-1) + i * (xMax + 1) / steps).toFixed(3));
            xValues.push(x);

            let approx = 0;
            for (let k = 0; k < nMax; k++) {
                const coeff = factorial(2*k)/(Math.pow(4,k)*Math.pow(factorial(k),2)*(2*k+1));
                approx += coeff * Math.pow(x, 2*k+1);
            }
            const arccosApprox = Math.PI/2 - approx;
            fSeries.push(arccosApprox);
            fExact.push(Math.acos(x));
        }

        // график
        if (functionChart) functionChart.destroy();
        functionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // х
                datasets: [
                    {
                        label: `Ряд (n=${nMax})`,
                        data: [], // у
                        borderColor: '#1f77b4',
                        backgroundColor: 'rgba(31,119,180,0.2)',
                        fill: false,
                        tension: 0.3
                    },
                    {
                        label: 'Точная функция',
                        data: [], // у
                        borderColor: '#ff7f0e',
                        backgroundColor: 'rgba(255,127,14,0.2)',
                        fill: false,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                animation: { duration: 0 }, 
                plugins: {
                    title: { display: true, text: 'Сравнение ряда и точной функции arccos(x)', color: '#1f77b4', font: { size: 18 } },
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'line',
                                yMin: 0.5,
                                yMax: 0.5,
                                borderColor: 'green',
                                borderWidth: 2,
                                label: {
                                    content: 'Уровень eps',
                                    enabled: true,
                                    position: 'center'
                                }
                            }
                        }
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'x', color: '#1f77b4', font: { size: 14 } } },
                    y: { title: { display: true, text: 'f(x)', color: '#1f77b4', font: { size: 14 } } }
                }
            }
        });

        let index = 0;
        const interval = setInterval(() => {
            if (index >= xValues.length) {
                clearInterval(interval);
                buildTable(xValues, fSeries, fExact, nMax); 
                return;
            }

            functionChart.data.labels.push(xValues[index]);
            functionChart.data.datasets[0].data.push(fSeries[index]);
            functionChart.data.datasets[1].data.push(fExact[index]);
            functionChart.update('none');
            index++;
        }, 50); 
    });

    document.getElementById('saveChart').addEventListener('click', () => {
        if (!functionChart) return;
        const link = document.createElement('a');
        link.download = 'chart.png';
        link.href = functionChart.toBase64Image();
        link.click();
    });

    function factorial(n) {
        if (n === 0 || n === 1) return 1;
        let res = 1;
        for (let i = 2; i <= n; i++) res *= i;
        return res;
    }

    function buildTable(xValues, fSeries, fExact, nMax) {
        let tableHTML = '<table><tr><th>x</th><th>n</th><th>f(x) ряд</th><th>f(x) точная</th><th>eps</th></tr>';
        for (let i = 0; i < xValues.length; i++) {
            const eps = Math.abs(fSeries[i] - fExact[i]);
            tableHTML += `<tr>
                <td>${xValues[i]}</td>
                <td>${nMax}</td>
                <td>${fSeries[i].toFixed(5)}</td>
                <td>${fExact[i].toFixed(5)}</td>
                <td>${eps.toExponential(2)}</td>
            </tr>`;
        }
        tableHTML += '</table>';
        tableContainer.innerHTML = tableHTML;
    }
});
