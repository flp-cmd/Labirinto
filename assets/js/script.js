var timestamp = null;

document.addEventListener("DOMContentLoaded", async () => {
    buildChart();

    setInterval(() => {
        buildChart();
    }, 2000)
})

async function buildChart() {
    const data = await fetch("assets/json/treeData.json").then((resp) => resp.json());
    const treeData = data.treeNodes ?? null;
    
    if(!treeData || data.timestamp === timestamp) return;

    [openL, closedL] = getOpenAndClosedList(data.interations_lists);
    console.log([openL, closedL])
    buildOpenAndClosedList(openL, closedL);

    timestamp = data.timestamp;
    
    const chart = echarts.init(document.getElementById('chart'));

    const option = {
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove',
            formatter: function (params) {
                const data = params.data;
                const value = data.value;
                return `<b>Atual:</b> ${value[0]}<br><b>Anterior:</b> ${value[1] || "--"}<br><b>f(a):</b> ${value[2]}`;
            }
        },
        series: [
            {
                type: 'tree',
                data: [convertData(treeData)],
                top: '20%',
                bottom: '5%',
                left: '10%',
                right: '10%',
                symbol: 'none',
                orient: 'vertical',
                expandAndCollapse: true,
                initialTreeDepth: getMaxDepth(treeData),
                layout: 'orthogonal',
                label: {
                    position: 'top',
                    verticalAlign: 'middle',
                    align: 'center',
                    fontSize: 12,
                    fontWeight: 'bold',
                    color: '#333',
                    formatter: function (params) {
                        const value = params.data.value;
                        return `${value[0]} | ${value[1] || "--"} | ${value[2].toFixed(2)}`;
                    }
                },
                leaves: {
                    label: {
                        position: 'bottom',
                        verticalAlign: 'middle',
                        align: 'center',
                        fontSize: 12,
                        fontWeight: 'bold',
                        color: '#333'
                    }
                },
                emphasis: {
                    focus: 'descendant'
                },
                lineStyle: {
                    color: '#ccc',
                    width: 1,
                    curveness: 0
                }
            }
        ]
    };

    chart.setOption(option);
}

function buildOpenAndClosedList(openL, closedL) {
    const container = document.getElementById("openAndClosedList");
    container.innerHTML = "";

    for(let i = 0; i < openL.length; i++) {
        let openStr = "";
        let closedStr = "";

        for(let j = 0; j < openL[i].length; j++) {
            openStr += openL[i][j] + " ";
        }

        for(let k = 0; k < closedL[i].length; k++) {
            closedStr += closedL[i][k] + " ";
        }

        const tr = document.createElement("tr");
        const tdOpen = document.createElement("td");
        const tdClosed = document.createElement("td");
        tdOpen.textContent = openStr;
        tdClosed.textContent = closedStr;
        tr.appendChild(tdOpen);
        tr.appendChild(tdClosed)
        container.appendChild(tr);
    }
}

function getOpenAndClosedList(lists) {
    const openL = lists["open_list"];
    const closedL = lists["closed_list"];
    const newOpenL = [];
    const newClosedL = [];

    newOpenL.push(openL[1]);
    newClosedL.push(closedL[0]);

    let close = true;
    let open = false;

    for(let i = 1; i < openL.length; i++) {
        if(close) {
            const currOpen = openL[i];
            const currClosed = closedL[i];
            const newOpenItem = removeDuplicates(currOpen, currClosed);
            newOpenL.push(newOpenItem);
            newClosedL.push(currClosed);
            open = true;
            close = false;
        } else if(open) {
            const currOpen = openL[i];
            const currClosed = closedL[i - 1];
            newOpenL.push(currOpen);
            newClosedL.push(currClosed);
            open = false;
            close = true;
        }
    }

    return [newOpenL, newClosedL]
}

function removeDuplicates(arr1, arr2) {
  const result = arr1.filter((value) => !arr2.includes(value));
  return result;
}

function convertData(data) {
    const result = {
        name: data.name,
        value: [data.name, data.parent, data.evaluation],
        children: []
    };

    if (data.children && data.children.length > 0) {
        data.children.forEach(child => {
            result.children.push(convertData(child));
        });
    }

    return result;
}

function getMaxDepth(data) {
    let maxDepth = 0;

    if (data.children && data.children.length > 0) {
        data.children.forEach(child => {
            const depth = getMaxDepth(child);
            maxDepth = Math.max(maxDepth, depth);
        });
    }

    return maxDepth + 1;
}

// Nós Abertos       Nós Fechados
// 6, 3              1
// 3                 1, 6
// 11, 8, 3          1, 6
// 8, 3              1, 6, 11
// 12, 16, 8, 3      1, 6, 11
// 16, 8, 3          1, 6, 11, 12
// 22, 8, 3          1, 6, 11, 12
// 22, 3             1, 6, 11, 12, 8
// 10, 22, 3         1, 6, 11, 12, 8
// 10, 22            1, 6, 11, 12, 8, 3
// 4, 10, 22         1, 6, 11, 12, 8, 3
// 10, 22            1, 6, 11, 12, 8, 3, 4
// 5, 10, 22         1, 6, 11, 12, 8, 3, 4
// 10, 22            1, 6, 11, 12, 8, 3, 4, 5
// 10, 22            1, 6, 11, 12, 8, 3, 4, 5
// 10