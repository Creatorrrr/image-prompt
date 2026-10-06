
(() => {
const root=document.getElementById("palette-research");
const payload=JSON.parse(document.getElementById("research-data").textContent);
const cards=payload.cards;
const byId=new Map(cards.map(c=>[c.seed_id,c]));
const sources=new Map(payload.sources.map(s=>[s.source_id,s]));
const selected=new Set([8,9]);
const search=root.querySelector("#search"),group=root.querySelector("#group"),priority=root.querySelector("#priority");
const grid=root.querySelector("#grid"),compare=root.querySelector("#compare"),count=root.querySelector("#count"),selectionStatus=root.querySelector("#selection-status");
const esc=x=>String(x).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
const chips=c=>'<div class="swatches" aria-label="'+esc(c.colors.map(x=>x.hex).join(", "))+'">'+c.colors.map(x=>'<span class="swatch" style="--chip:'+x.hex+'"></span>').join("")+'</div><div class="chip-labels">'+c.colors.map(x=>'<span>'+x.hex+'</span>').join("")+'</div>';
const groups=new Map(cards.map(c=>[c.group_id,c.group_label_ko]));
for(const [id,label]of groups){const o=document.createElement("option");o.value=id;o.textContent=label.split(":")[0];group.append(o);}
function detail(c){
 const list=c.owners.map(o=>'<li><span class="dot" style="--chip:'+o.hex_reference+'"></span><strong>'+esc(o.role_ko)+'</strong><br>'+esc(o.owner_phrase_en)+'</li>').join("");
 const stats=c.colors.map(x=>'<tr><td>'+x.hex+'</td><td>'+x.oklch.L.toFixed(3)+'</td><td>'+x.oklch.C.toFixed(3)+'</td></tr>').join("");
 const links=c.source_refs.map(id=>{const s=sources.get(id);return '<li><a href="'+esc(s.url)+'" target="_blank" rel="noreferrer">'+esc(s.source_id+" "+s.title)+'</a><br><small>'+esc(s.limit_ko)+'</small></li>'}).join("");
 return '<article class="detail"><h3>'+esc(c.semantic_id+" · "+c.label_ko)+'</h3>'+chips(c)+'<p>'+esc(c.meaning_ko)+'</p><ul>'+list+'</ul><p><strong>관찰할 관계</strong><br>'+esc(c.relation_en)+'</p><p><strong>오인 경계</strong><br>'+esc(c.failure_ko)+'</p><details><summary>계산값과 출처</summary><div class="metrics"><table><thead><tr><th>색 코드</th><th>Oklab L</th><th>Oklch C</th></tr></thead><tbody>'+stats+'</tbody></table></div><ul>'+links+'</ul></details></article>';
}
function render(){
 const q=search.value.trim().toLocaleLowerCase();
 const filtered=cards.filter(c=>(!group.value||c.group_id===Number(group.value))&&(!priority.value||c.priority===priority.value)&&(!q||c.search_text.includes(q)));
 count.textContent=filtered.length+" / 100개 조합";
 selectionStatus.textContent="비교 "+selected.size+" / 4";
 grid.innerHTML=filtered.length?filtered.map(c=>'<article class="palette"><button type="button" data-id="'+c.seed_id+'" aria-pressed="'+selected.has(c.seed_id)+'">'+esc(c.semantic_id+" · "+c.label_ko)+'</button>'+chips(c)+'<div class="meta">'+esc(c.priority+" · "+c.group_label_ko.split(":")[0])+'</div></article>').join(""):'<p class="empty">일치하는 조합이 없습니다.</p>';
 compare.innerHTML=[...selected].map(id=>detail(byId.get(id))).join("");
}
grid.addEventListener("click",event=>{
 const b=event.target.closest("button[data-id]");if(!b)return;
 const id=Number(b.dataset.id);
 if(selected.has(id))selected.delete(id);
 else if(selected.size<4)selected.add(id);
 else{selectionStatus.textContent="최대 4개입니다. 선택한 조합 하나를 먼저 해제하세요.";return;}
 render();
});
for(const el of [search,group,priority])el.addEventListener("input",render);
root.querySelector("#clear").addEventListener("click",()=>{selected.clear();render()});
render();
})();
