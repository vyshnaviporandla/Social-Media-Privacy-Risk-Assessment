let questions=[],answers={},index=0,chart=null;
const $=id=>document.getElementById(id);
async function load(){
  questions=await fetch("/api/questions").then(r=>r.json());
  render();
  const c=await fetch("/api/privacy-checklist").then(r=>r.json());
  $("checklist").innerHTML=c.map(x=>`<div>✓ ${x}</div>`).join("");
  refreshStats();
}
function render(){
  const q=questions[index];
  $("counter").textContent=`Question ${index+1} of ${questions.length}`;
  $("progressBar").style.width=`${((index+1)/questions.length)*100}%`;
  $("questionBox").innerHTML=`<div class="question">${q.text}</div>`+
    q.options.map(o=>`<label class="option"><input type="radio" name="answer" value="${o}" ${answers[q.id]===o?"checked":""}>${o}</label>`).join("");
  $("prev").disabled=index===0;
  $("next").textContent=index===questions.length-1?"Submit Assessment":"Next";
}
$("prev").onclick=()=>{if(index>0){save();index--;render()}};
$("next").onclick=()=>{if(!save())return;if(index<questions.length-1){index++;render()}else submit()};
function save(){
  const q=questions[index], picked=document.querySelector('input[name="answer"]:checked');
  if(!picked){alert("Please select an answer.");return false}
  answers[q.id]=picked.value;return true;
}
async function submit(){
  const r=await fetch("/api/assessment",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answers})});
  const data=await r.json();if(!r.ok){alert(data.error||"Assessment failed.");return}
  $("questionnaire").classList.add("hidden");$("result").classList.remove("hidden");
  $("score").textContent=data.overall_score;$("level").textContent=data.risk_level;
  $("findings").innerHTML=data.findings.length?data.findings.map(f=>`<div class="finding"><b>${f.category}</b><br>${f.finding}</div>`).join(""):"<p>No major findings above the configured threshold.</p>";
  $("recommendations").innerHTML=data.recommendations.length?data.recommendations.map(x=>`<div class="rec"><b>${x.category}</b><br>${x.recommendation}</div>`).join(""):"<p>Your current responses generated no high-priority recommendations.</p>";
  draw(data.category_scores);refreshStats();
}
function draw(scores){
  if(chart)chart.destroy();
  chart=new Chart($("chart"),{type:"radar",data:{labels:Object.keys(scores),datasets:[{label:"Category Risk",data:Object.values(scores),fill:true}]},options:{scales:{r:{beginAtZero:true,max:100}}}});
}
$("simulate").onclick=async()=>{
 const r=await fetch("/api/assessment/simulate-improvement",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answers})});
 const d=await r.json();$("simulationResult").innerHTML=`<h3>${d.current_score} → ${d.simulated_score}</h3><p>${d.current_level} → ${d.simulated_level}. Improvement: ${d.improvement} points.</p><small>${d.note}</small>`;
};
$("restart").onclick=()=>{answers={};index=0;$("result").classList.add("hidden");$("questionnaire").classList.remove("hidden");render()};
async function refreshStats(){const d=await fetch("/api/dashboard/stats").then(r=>r.json());$("total").textContent=d.total_assessments;$("avg").textContent=d.average_score;$("levels").textContent=Object.keys(d.risk_levels).length}
load();
