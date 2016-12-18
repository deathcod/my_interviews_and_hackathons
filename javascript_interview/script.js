get_value();

function get_value()
{
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() 
	{
		if (this.readyState == 4 && this.status == 200) 
		{
			var data = this.responseText;
	    	initiate(JSON.parse(data));
		}
	};
	xhttp.open("GET", "input.json", true);
	xhttp.send();
}

function initiate(myArr)
{
	console.log(myArr);
	var v_dist = {};
	var v_time = {};
	var v_connect = {};
	var visited_connect = {};
	var visited = [];

	for(var key1 in myArr)
	{
		visited[key1]=0;
		if(!(key1 in v_dist))
		{
			v_dist[key1]={};
			v_time[key1]={};
			v_connect[key1]=[];
		}
		for(var key2 in myArr[key1])
		{
			v_connect[key1].push(key2);
			visited[key2]=0;
			v_dist[key1][key2] = myArr[key1][key2][1];
			v_time[key1][key2] = myArr[key1][key2][0] / myArr[key1][key2][1];
		}
	}

	var len=0;
	for(var key in visited)
	{
		visited_connect[key] = [0,0];
		len++;
	}
	//All paths
	console.log(len);
	floyd_warshal(v_connect, visited_connect,visited,len,'S','U');

	for(var key in visited)
		visited[key] = 1e9;
	//Distance Optimal
	//dijisktra_algo(v_dist,visited,'S');


	//Time Optimal
	for(var key in visited)
		visited[key] = 1e9;
	//dijisktra_algo(v_time,visited,'S');
}

function dijisktra_algo(v,visited,source)
{
	var queue = [];
	var visited_path = {};

	queue.push([source,0]);
	visited[source]=0;
	visited_path[source] = [];
	while(queue.length)
	{	
		var front = queue.shift();
		console.log(front);
		var x = front[0];
		for(var i in v[x])
		{
			console.log("\t"+i);
			if(visited[i] > visited[x]+v[x][i] && i != source)
			{
				var w = [i,visited[i]];
				console.log("w:\t\t"+w);
				var index = queue.indexOf(w);
				console.log("index:\t\t"+index);
				if(index!=-1)
					queue.splice(index);
				console.log("q.l:\t\t"+queue.length);
				visited[i] = visited[x]+v[x][i];
				w[1] = visited[i];
				queue.push(w);
				console.log("w:\t\t"+w);
				console.log("q.l:\t\t"+queue.length);
				visited_path[i]=[];
				for(var key in visited_path[x])
					visited_path[i].push(visited_path[x][key]);
				visited_path[i].push(x);
			}
		}
	}
	for(var key in visited)
		console.log(key +" "+visited_path[key]);
	console.log("The shortest val:\t"+visited['U']);
	console.log("The shortest path:\t"+visited_path['U']);
}

function floyd_warshal(v_connect, visited_connect,visited,len,source,destination)
{
	visited_connect['S'][0]++;
	visited_connect['U'][1]++;
	while(len--)
	{

		for( var i in v_connect)
		{
			//console.log(i);
			for( var j in v_connect[i])
			{
				//console.log("\t"+v_connect[i][j]);
				var curr_node = v_connect[i][j];
				visited_connect[curr_node][0]|=visited_connect[i][0];
				visited_connect[curr_node][1]|=visited_connect[i][1];
			}
		}
	}
	//nodes that are touched
	var connected_nodes = [];
	for(var i in visited_connect)
	{
		//console.log(i+":\t\t"+visited_connect[i]);
		if(visited_connect[i][0] && visited_connect[i][1])
			connected_nodes.push(i);
	}

	var queue = [];
	queue.push(source);
	visited[source]=1;
	while(queue.length)
	{
		console.log("------------------------");
		var front = queue.shift();
		for(var i in v_connect[front])
		{
			var curr_node = v_connect[front][i];
			if(connected_nodes.indexOf(curr_node)>=0)
			{
				/* 
				so here u can show the animation for 
				connection like S--->T
				S  =  front
				T  =  curr_node
				*/
				console.log(front+" -----> "+curr_node);
			}
			if(visited[curr_node]==0 && connected_nodes.indexOf(curr_node)>=0)
			{
				visited[curr_node]=1;
				queue.push(curr_node);
			}
		}
	}
}