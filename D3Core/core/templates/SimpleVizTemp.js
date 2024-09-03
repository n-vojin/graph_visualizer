// SimpleVizTemp.js
(function() {
    let simulation;
    let svg, g, birdSvg, birdG;
    let width = 900, height = 600;    let birdWidth = 300, birdHeight = 200;

    function initializeGraph() {
        d3.select("#graph").selectAll("*").remove();
        d3.select("#bird-view").selectAll("*").remove();

        svg = d3.select("#graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        g = svg.append("g");

        birdSvg = d3.select("#bird-view")
            .append("svg")
            .attr("width", birdWidth)
            .attr("height", birdHeight);

        birdG = birdSvg.append("g");

        // Add zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {
                g.attr("transform", event.transform);
                updateBirdViewport(event.transform);
            });

        svg.call(zoom);

        simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(d => d.id).distance(150))
            .force("charge", d3.forceManyBody().strength(-100))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collide", d3.forceCollide().radius(30));

        return { g, birdG };
    }

    function loadGraph() {
        const { g, birdG } = initializeGraph();

        $.ajax({
            url: '/get_graph_data/',
            method: 'GET',
            dataType: 'json',
            success: function(graph) {
                const nodes = Object.values(graph.nodes).map(node => ({
                    id: node.node_id,
                    x: Math.random() * width,
                    y: Math.random() * height
                }));

                const links = graph.edges.map(edge => ({
                    source: edge.source.node_id,
                    target: edge.destination.node_id
                }));

                const link = g.append("g")
                    .attr("stroke", "#999")
                    .attr("stroke-opacity", 0.6)
                    .selectAll("line")
                    .data(links)
                    .join("line")
                    .attr("stroke-width", 2);

                const node = g.append("g")
                    .attr("stroke", "#fff")
                    .attr("stroke-width", 1.5)
                    .selectAll("circle")
                    .data(nodes)
                    .join("circle")
                    .attr("r", 10)
                    .attr("fill", "#69b3a2")
                    .call(drag(simulation));

                node.append("title")
                    .text(d => d.id);

                const labels = g.append("g")
                    .attr("class", "labels")
                    .selectAll("text")
                    .data(nodes)
                    .enter()
                    .append("text")
                    .text(d => d.id)
                    .attr("font-size", "10px")
                    .attr("dx", 12)
                    .attr("dy", 4);

                // Bird's eye view elements
                const birdLink = birdG.append("g")
                    .attr("stroke", "#999")
                    .attr("stroke-opacity", 0.6)
                    .selectAll("line")
                    .data(links)
                    .join("line")
                    .attr("stroke-width", 1);

                const birdNode = birdG.append("g")
                    .selectAll("circle")
                    .data(nodes)
                    .join("circle")
                    .attr("r", 2)
                    .attr("fill", "#69b3a2");

                // Add viewport rectangle to bird's eye view
                const viewport = birdSvg.append("rect")
                    .attr("stroke", "red")
                    .attr("stroke-width", 2)
                    .attr("fill", "none");

                simulation
                    .nodes(nodes)
                    .on("tick", ticked);

                simulation.force("link")
                    .links(links);

                function ticked() {
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);

                    labels
                        .attr("x", d => d.x)
                        .attr("y", d => d.y);

                    // Update bird's eye view
                    birdLink
                        .attr("x1", d => d.source.x * birdWidth / width)
                        .attr("y1", d => d.source.y * birdHeight / height)
                        .attr("x2", d => d.target.x * birdWidth / width)
                        .attr("y2", d => d.target.y * birdHeight / height);

                    birdNode
                        .attr("cx", d => d.x * birdWidth / width)
                        .attr("cy", d => d.y * birdHeight / height);
                }

                // Initial update of bird's eye view viewport
                updateBirdViewport(d3.zoomIdentity);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Error fetching graph data:", textStatus, errorThrown);
            }
        });
    }

    function updateBirdViewport(transform) {
        const viewport = birdSvg.select("rect");
        const scale = transform.k;
        const translateX = transform.x;
        const translateY = transform.y;

        const vpWidth = birdWidth / scale;
        const vpHeight = birdHeight / scale;
        const vpX = (-translateX / scale) * (birdWidth / width);
        const vpY = (-translateY / scale) * (birdHeight / height);

        viewport
            .attr("x", vpX)
            .attr("y", vpY)
            .attr("width", vpWidth)
            .attr("height", vpHeight);
    }

    function drag(simulation) {
        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    // Expose the loadGraph function to the global scope
    window.loadGraph = loadGraph;

    // Initialize the graph when the document is ready
    $(document).ready(function() {
        $("#loadGraphBtn").click(loadGraph);
        loadGraph(); // Initial load
    });
})();