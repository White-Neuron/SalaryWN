const ctx_sum = document.getElementById('summary');
const ctx_sum_all = document.getElementById('sumall');
const ctx_giolam = document.getElementById('giolam');
const ctx_giolam_all = document.getElementById('giolamall');
const select_emp = document.getElementById('select-employee')

function shortenString(inputString) {
    const hyphenIndex = inputString.indexOf("-");

    if (hyphenIndex !== -1) {
        // Found a hyphen, extract characters up to that point
        return inputString.substring(0, hyphenIndex) + "..." + inputString.slice(-1);
    } else {
        // No hyphen found, return the original string
        return inputString;
    }
}


// fetch(`/admin/DashBoard/api/salary/chart_summary/sdd001/`)
//     .then(response => response.json())
//     .then(data => {
//         console.log(data)
//             new Chart(ctx_sum, {
//                     // type: 'bar',
//                 data: {
//                         datasets: data.datasets,
//                         labels: data.labels
//                     },
//                     options: {
//                         responsive: true,
//                         scales: {
//                             y: {
//                                 display: true,
//                                 ticks: data.y_ticks,
//                                 title: data.y_label,
//                                 beginAtZero: true,
//                             },
//                             x: {
//                                 display: true,
//                                 ticks: data.x_ticks,
//                                 title: data.x_label,
//                             }

//                         },
//                         plugins: {
//                             title: data.title,
//                         }
//                     }
//                 });
//             })
//             .catch(error => console.error('Error fetching data:', error));

fetch(`/admin/DashBoard/api/get_employees/`)
    .then(response => response.json())
    .then(data => {
        console.log(data.data)
        const html = `<label for="group-chart-select" style="font-weight:bold;font-size:18px">Select group: </label><select id="group-chart-select" style="min-width:100px;font-weight:bold;margin-left:10px;padding:5px 10px;height:40px;font-size:18px">${data.data.map((item, index) => `<option  value=${item.mnv} ${index === 0 ? "selected" : ""}>${item.mnv} - ${item.name}</option>`).join("")}</select>`
        select_emp.innerHTML= html

        const selectEMP = document.getElementById("group-chart-select")
        // console.log(selectEMP.value)
        render_chart(selectEMP.value)
        selectEMP.addEventListener('change', () => {
            console.log(selectEMP.value)
            render_chart(selectEMP.value)
        })
        function render_chart(mnv) {
            fetch(`/admin/DashBoard/api/salary/chart_summary/${mnv}/`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    const html = `<canvas id="summary-${mnv}"></canvas>`
                    ctx_sum.innerHTML = html
                    const ctx_render = document.getElementById(`summary-${mnv}`)
                        new Chart(ctx_render, {
                                // type: 'bar',
                            data: {
                                    datasets: data.datasets,
                                    labels: data.labels
                                },
                                options: {
                                    responsive: true,
                                    scales: {
                                        y: {
                                            display: true,
                                            ticks: data.y_ticks,
                                            title: data.y_label,
                                            beginAtZero: true,
                                        },
                                        x: {
                                            display: true,
                                            ticks: data.x_ticks,
                                            title: data.x_label,
                                        }

                                    },
                                    plugins: {
                                        title: data.title,
                                    }
                                }
                            });
                        })
                        .catch(error => console.error('Error fetching data:', error));
    
        
            fetch(`/admin/DashBoard/api/giolam/chart_giolam/${mnv}/`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    const html = `<canvas id="giolam-${mnv}"></canvas>`
                    ctx_giolam.innerHTML = html
                    const ctx_render_giolam = document.getElementById(`giolam-${mnv}`)
                        new Chart(ctx_render_giolam, {
                        // type: 'bar',
                        data: {
                            datasets: data.datasets,
                            labels: data.labels
                        },
                        options: {
                            responsive: true,
                            scales: {
                                y: {
                                    display: true,
                                    ticks: data.y_ticks,
                                    title: data.y_label,
                                    beginAtZero: true,
                                },
                                x: {
                                    display: true,
                                    ticks: data.x_ticks,
                                    title: data.x_label,
                                }
            
                            },
                            plugins: {
                                title: data.title,
                            }
                        }
                    });
                })
                .catch(error => console.error('Error fetching data:', error));
            }
        })
        

fetch(`/admin/DashBoard/api/salary/chart_summary_all/`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        new Chart(ctx_sum_all, {
            // type: 'bar',
            data: {
                datasets: data.datasets,
                labels: data.labels
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        display: true,
                        ticks: data.y_ticks,
                        title: data.y_label,
                        beginAtZero: true,
                    },
                    x: {
                        display: true,
                        ticks: data.x_ticks,
                        title: data.x_label,
                    }

                },
                plugins: {
                    title: data.title,
                }
            }
        });
    })
    .catch(error => console.error('Error fetching data:', error));

// fetch(`/admin/DashBoard/api/giolam/chart_giolam/sdd003/`)
//     .then(response => response.json())
//     .then(data => {
//         console.log(data)
//         new Chart(ctx_giolam, {
//             // type: 'bar',
//             data: {
//                 datasets: data.datasets,
//                 labels: data.labels
//             },
//             options: {
//                 responsive: true,
//                 scales: {
//                     y: {
//                         display: true,
//                         ticks: data.y_ticks,
//                         title: data.y_label,
//                         beginAtZero: true,
//                     },
//                     x: {
//                         display: true,
//                         ticks: data.x_ticks,
//                         title: data.x_label,
//                     }

//                 },
//                 plugins: {
//                     title: data.title,
//                 }
//             }
//         });
//     })
//     .catch(error => console.error('Error fetching data:', error));


    fetch(`/admin/DashBoard/api/giolam/chart_giolam_all/`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        new Chart(ctx_giolam_all, {
            // type: 'bar',
            data: {
                datasets: data.datasets,
                labels: data.labels
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        display: true,
                        ticks: data.y_ticks,
                        title: data.y_label,
                        beginAtZero: true,
                    },
                    x: {
                        display: true,
                        ticks: data.x_ticks,
                        title: data.x_label,
                    }

                },
                plugins: {
                    title: data.title,
                }
            }
        });
    })
    .catch(error => console.error('Error fetching data:', error));
