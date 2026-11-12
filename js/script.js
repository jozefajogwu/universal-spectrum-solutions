/* USSL — Direction B */

(function(){
  'use strict';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- split the headline into words ---- */
  function split(el){
    if(el.dataset.split) return;
    el.dataset.split='1';
    var frag=document.createDocumentFragment(), n=0;
    Array.prototype.slice.call(el.childNodes).forEach(function(node){
      if(node.nodeType===1 && node.classList && node.classList.contains('circled')){
        var w=document.createElement('span'); w.className='w';
        var i=document.createElement('i');
        i.appendChild(node.cloneNode(true));
        i.style.transitionDelay=(n*60)+'ms'; n++;
        w.appendChild(i); frag.appendChild(w);
        frag.appendChild(document.createTextNode(' '));
        return;
      }
      (node.textContent||'').split(/\s+/).filter(Boolean).forEach(function(word){
        var w=document.createElement('span'); w.className='w';
        var i=document.createElement('i');
        i.textContent=word;
        i.style.transitionDelay=(n*60)+'ms'; n++;
        w.appendChild(i); frag.appendChild(w);
        frag.appendChild(document.createTextNode(' '));
      });
    });
    el.textContent='';
    el.appendChild(frag);
  }

  /* ---- count up ---- */
  function countUp(el){
    var target=parseInt(el.dataset.count,10);
    if(isNaN(target)) return;
    if(reduce){ el.textContent=target; return; }
    var start=null, dur=1100;
    function step(ts){
      if(!start) start=ts;
      var p=Math.min((ts-start)/dur,1);
      var eased=1-Math.pow(1-p,3);
      el.textContent=Math.round(target*eased);
      if(p<1) requestAnimationFrame(step);
    }
    el.textContent='0';
    requestAnimationFrame(step);
  }

  /* ---- reveal groups ---- */
  var SOLO='.hero .lede,.hero-actions,.center h2,.center .lede,.sec-title h2,.sec-title .lede,.help-copy,.cta,.trusted,.qmark,.quote-body,.who,.dots,.copy,.split > div,.note,form,.banner .eyebrow';
  var GROUPS=[['.stats > div','pop'],['.svc .card',''],['.grid-4 .tile','pop'],
              ['.why .b',''],['.orgs span','pop'],['.foot > div',''],
              ['.entries .entry',''],['.people .person','pop'],['.steps .step','pop'],
              ['.caps .cap','pop'],['.packs .pack',''],['.logos div','pop'],
              ['.pillrow span','pop'],['.offices .office','']];

  function arm(){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting) return;
        var t=e.target;
        if(t.tagName==='H1'){
          t.classList.add('h-in');
          var c=t.querySelector('.circled');
          if(c) setTimeout(function(){c.classList.add('drawn')},300);
        } else {
          t.classList.add('in');
          t.querySelectorAll('[data-count]').forEach(countUp);
        }
        io.unobserve(t);
      });
    },{threshold:.12,rootMargin:'0px 0px -5% 0px'});

    document.querySelectorAll('h1:not(.htitle)').forEach(function(el){ split(el); io.observe(el); });

    document.querySelectorAll(SOLO).forEach(function(el){
      el.classList.add('rv'); io.observe(el);
    });

    GROUPS.forEach(function(g){
      document.querySelectorAll(g[0]).forEach(function(el,i){
        el.classList.add('rv'); if(g[1]) el.classList.add(g[1]);
        el.style.transitionDelay=(i*80)+'ms';
        io.observe(el);
      });
    });
  }


  /* ---- mobile menu ---- */
  (function(){
    var btn=document.querySelector('.menu'), nav=document.querySelector('nav');
    if(!btn||!nav) return;
    btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click',function(){
      var open=nav.classList.toggle('open');
      btn.setAttribute('aria-expanded',open?'true':'false');
    });
  })();


  /* ---- hero slider ---- */
  (function(){
    var slides=[].slice.call(document.querySelectorAll('.slide'));
    var dots=[].slice.call(document.querySelectorAll('.hdot'));
    if(slides.length<2) return;
    var i=0, timer=null, DUR=7000;
    function go(n){
      i=(n+slides.length)%slides.length;
      slides.forEach(function(s,k){s.classList.toggle('on',k===i)});
      dots.forEach(function(d,k){d.classList.toggle('on',k===i)});
    }
    function start(){ if(!reduce){ stop(); timer=setInterval(function(){go(i+1)},DUR); } }
    function stop(){ if(timer) clearInterval(timer); }
    dots.forEach(function(d){
      d.addEventListener('click',function(){ go(+d.dataset.go); start(); });
    });
    var hero=document.querySelector('.hero');
    if(hero){
      hero.addEventListener('mouseenter',stop);
      hero.addEventListener('mouseleave',start);
    }
    document.addEventListener('visibilitychange',function(){
      document.hidden ? stop() : start();
    });
    start();
  })();


  /* ---- live contour-wave field (canvas) ---- */
  (function(){
    var canvases = [].slice.call(document.querySelectorAll('[data-waves]'));
    if(!canvases.length) return;

    function build(cv){
      var ctx = cv.getContext('2d', {alpha:true});
      if(!ctx) return;
      var w=0, h=0, dpr=1, raf=null, running=false, t0=null, visible=true;
      var LINES = 24;

      function size(){
        dpr = Math.min(window.devicePixelRatio||1, 2);
        w = cv.clientWidth; h = cv.clientHeight;
        if(!w||!h) return false;
        cv.width = Math.round(w*dpr);
        cv.height = Math.round(h*dpr);
        ctx.setTransform(dpr,0,0,dpr,0,0);
        return true;
      }

      function draw(ms){
        if(!w||!h) return;
        var t = ms*0.001;
        ctx.clearRect(0,0,w,h);
        ctx.lineCap = 'round';
        var step = w > 900 ? 7 : 11;

        for(var i=0;i<LINES;i++){
          var u = i/(LINES-1);
          // slow breathing of the whole band
          var breathe = 1 + 0.18*Math.sin(t*0.21 + u*1.6);
          var amp = h*(0.040 + 0.125*Math.sin(Math.PI*u)) * breathe;
          var yb  = h*(0.13 + 0.74*u) + h*0.03*Math.sin(t*0.17 + u*2.3);
          var ph  = u*2.4 + t*0.36;
          var freq= 1.45 + 0.6*Math.sin(u*3.1 + t*0.08);

          var glow = Math.max(0, 1 - Math.abs(u-0.42)/0.34);
          glow *= 0.78 + 0.22*Math.sin(t*0.55 + u*5.0);   // shimmer along the crest

          ctx.beginPath();
          for(var x=0;x<=w+step;x+=step){
            var q = x/w;
            var y = yb
              + amp*Math.sin(q*Math.PI*freq*2 + ph)
              + amp*0.30*Math.sin(q*Math.PI*5.2 + ph*1.7 + t*0.52)
              + amp*0.18*Math.sin(q*Math.PI*1.3 - t*0.27 + u*4.0);
            if(x===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
          }
          if(glow>0.60){
            ctx.strokeStyle='rgba(165,201,255,'+(0.12+0.58*glow).toFixed(3)+')';
            ctx.lineWidth=1.6;
          } else if(glow>0.26){
            ctx.strokeStyle='rgba(93,147,255,'+(0.10+0.50*glow).toFixed(3)+')';
            ctx.lineWidth=1.2;
          } else {
            ctx.strokeStyle='rgba(47,95,196,'+(0.10+0.34*glow).toFixed(3)+')';
            ctx.lineWidth=1.0;
          }
          ctx.stroke();
        }
      }

      function frame(ms){
        if(t0===null) t0=ms;
        draw(ms - t0);
        raf = requestAnimationFrame(frame);
      }
      function start(){
        if(running || reduce || !visible) return;
        running = true; raf = requestAnimationFrame(frame);
      }
      function stop(){
        running = false;
        if(raf) cancelAnimationFrame(raf);
        raf = null;
      }

      if(!size()){
        requestAnimationFrame(function(){ if(size()) reduce ? draw(0) : start(); });
      } else if(reduce){
        draw(0);
      } else {
        start();
      }

      var rt;
      window.addEventListener('resize', function(){
        clearTimeout(rt);
        rt = setTimeout(function(){ if(size()){ reduce ? draw(0) : null; } }, 160);
      }, {passive:true});

      document.addEventListener('visibilitychange', function(){
        document.hidden ? stop() : start();
      });

      if('IntersectionObserver' in window){
        new IntersectionObserver(function(es){
          visible = es[0].isIntersecting;
          visible ? start() : stop();
        }, {threshold:0}).observe(cv);
      }
    }

    canvases.forEach(build);
  })();

  function init(){
    if(reduce){
      document.querySelectorAll('h1:not(.htitle)').forEach(function(e){e.classList.add('h-in')});
      document.querySelectorAll('[data-count]').forEach(countUp);
      return;
    }
    arm();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
