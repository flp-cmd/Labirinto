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
