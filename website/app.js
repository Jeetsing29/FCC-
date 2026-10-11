/**
 * Cloud-Based Website Hosting and Monitoring System Using AWS
 * Course: Fundamentals of Cloud Computing (B.Tech Second Year)
 * Vanilla JavaScript: Mobile Drawer, ScrollSpy, Sticky Navbar, Scroll-To-Top, & Telemetry Simulator
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Navbar & Scroll-To-Top Button
  const navbarWrapper = document.getElementById('navbarWrapper');
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // Sticky navbar elevation
    if (navbarWrapper) {
      if (scrollY > 30) {
        navbarWrapper.classList.add('scrolled');
      } else {
        navbarWrapper.classList.remove('scrolled');
      }
    }

    // Scroll-to-top button visibility
    if (scrollTopBtn) {
      if (scrollY > 320) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    }

    // ScrollSpy active link highlighting
    let currentSectionId = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        currentSectionId = section.getAttribute('id');
      }
    });

    if (currentSectionId) {
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSectionId}`) {
          link.classList.add('active');
        }
      });
    }
  }, { passive: true });

  // Scroll to top click
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 2. Mobile Hamburger Menu Toggle
  if (hamburgerBtn && navMenu) {
    hamburgerBtn.addEventListener('click', () => {
      const isExpanded = hamburgerBtn.getAttribute('aria-expanded') === 'true';
      hamburgerBtn.setAttribute('aria-expanded', String(!isExpanded));
      navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking a nav link or mobile cta
    const allMenuLinks = navMenu.querySelectorAll('a');
    allMenuLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (event) => {
      if (!navbarWrapper.contains(event.target) && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 3. Interactive Live Telemetry Simulator (Viva Demonstration Feature)
  const refreshMetricsBtn = document.getElementById('refreshMetricsBtn');
  const simulateSpikeBtn = document.getElementById('simulateSpikeBtn');
  const cpuNumber = document.getElementById('cpuNumber');
  const cpuProgress = document.getElementById('cpuProgress');
  const cpuAlarmBadge = document.getElementById('cpuAlarmBadge');
  const cpuStatusText = document.getElementById('cpuStatusText');
  const memNumber = document.getElementById('memNumber');
  const memProgress = document.getElementById('memProgress');
  const netNumber = document.getElementById('netNumber');
  const netProgress = document.getElementById('netProgress');
  const packetCount = document.getElementById('packetCount');
  const terminalLogs = document.getElementById('terminalLogs');
  const instanceStateBadge = document.getElementById('instanceStateBadge');

  function getTimestamp() {
    const now = new Date();
    return now.toTimeString().split(' ')[0] + ' UTC';
  }

  function addLog(type, message) {
    if (!terminalLogs) return;
    const line = document.createElement('div');
    line.className = 'log-entry';

    let tagClass = 'log-info';
    let tagLabel = '[INFO]';
    if (type === 'success') { tagClass = 'log-success'; tagLabel = '[OK]'; }
    if (type === 'warning') { tagClass = 'log-warning'; tagLabel = '[WARN]'; }
    if (type === 'alarm') { tagClass = 'log-alarm'; tagLabel = '[ALARM]'; }

    line.innerHTML = `<span class="log-time">[${getTimestamp()}]</span> <span class="${tagClass}">${tagLabel}</span> ${message}`;
    terminalLogs.appendChild(line);
    terminalLogs.scrollTop = terminalLogs.scrollHeight;
  }

  function setNormalState() {
    const cpuVal = (12.0 + Math.random() * 5.0).toFixed(1);
    const memVal = (30.0 + Math.random() * 3.5).toFixed(1);
    const netVal = (1.2 + Math.random() * 0.7).toFixed(2);
    const pps = Math.floor(1200 + Math.random() * 350);

    if (cpuNumber) cpuNumber.textContent = cpuVal;
    if (cpuProgress) {
      cpuProgress.style.width = `${cpuVal}%`;
      cpuProgress.style.backgroundColor = 'var(--accent-cyan)';
    }

    if (cpuAlarmBadge) {
      cpuAlarmBadge.className = 'status-pill status-ok';
      cpuAlarmBadge.textContent = 'OK (< 80%)';
    }

    if (cpuStatusText) {
      cpuStatusText.textContent = 'Normal Operations';
    }

    if (memNumber) memNumber.textContent = memVal;
    if (memProgress) memProgress.style.width = `${memVal}%`;

    if (netNumber) netNumber.textContent = netVal;
    if (netProgress) netProgress.style.width = `${Math.min(100, Math.floor(netVal * 20))}%`;
    if (packetCount) packetCount.textContent = `${pps.toLocaleString()} pkts/s`;

    if (instanceStateBadge) {
      instanceStateBadge.className = 'badge-status-running';
      instanceStateBadge.textContent = 'running';
    }
  }

  if (refreshMetricsBtn) {
    refreshMetricsBtn.addEventListener('click', () => {
      setNormalState();
      addLog('info', 'CloudWatch polled fresh metrics from EC2 hypervisor for i-0875444197e8dba94.');
      addLog('success', 'Reachability checks confirmed 2/2 Passed. Workload optimal.');
    });
  }

  if (simulateSpikeBtn) {
    simulateSpikeBtn.addEventListener('click', () => {
      const spikeCpu = (84.0 + Math.random() * 10.0).toFixed(1);
      const spikeMem = (70.0 + Math.random() * 6.0).toFixed(1);
      const spikeNet = (9.2 + Math.random() * 3.0).toFixed(2);
      const pps = Math.floor(9800 + Math.random() * 2500);

      if (cpuNumber) cpuNumber.textContent = spikeCpu;
      if (cpuProgress) {
        cpuProgress.style.width = `${spikeCpu}%`;
        cpuProgress.style.backgroundColor = 'var(--accent-red)';
      }

      if (cpuAlarmBadge) {
        cpuAlarmBadge.className = 'status-pill status-alarm';
        cpuAlarmBadge.textContent = 'ALARM (CPU > 80%)';
      }

      if (cpuStatusText) {
        cpuStatusText.textContent = 'High CPU Utilization Triggered!';
      }

      if (memNumber) memNumber.textContent = spikeMem;
      if (memProgress) memProgress.style.width = `${spikeMem}%`;

      if (netNumber) netNumber.textContent = spikeNet;
      if (netProgress) netProgress.style.width = '88%';
      if (packetCount) packetCount.textContent = `${pps.toLocaleString()} pkts/s`;

      if (instanceStateBadge) {
        instanceStateBadge.className = 'badge-status-alarm';
        instanceStateBadge.textContent = 'high-load';
      }

      addLog('warning', `Elevated HTTP request rate detected on Port 80. Network ingress: ${spikeNet} MB/s.`);
      addLog('alarm', `CloudWatch Alarm 'HighCPUUtilization-fcc-web-server' breached! Metric reached ${spikeCpu}%. State: ALARM.`);
      addLog('alarm', `Amazon SNS dispatched email notification to subscriber endpoint.`);

      // Automatically recover after 7 seconds
      setTimeout(() => {
        setNormalState();
        addLog('success', 'Traffic surge subsided. CPUUtilization returned to normal. CloudWatch Alarm state: OK.');
      }, 7000);
    });
  }

  // 4. Real User Monitoring (RUM) Telemetry (W3C Performance Navigation Timing)
  window.addEventListener('load', () => {
    setTimeout(() => {
      try {
        const perfEntries = performance.getEntriesByType('navigation');
        if (perfEntries && perfEntries.length > 0) {
          const nav = perfEntries[0];
          const ttfb = Math.round(nav.responseStart - nav.requestStart);
          const domComplete = Math.round(nav.domComplete - nav.startTime);
          if (ttfb >= 0 && domComplete >= 0) {
            addLog('info', `Real User Telemetry (RUM): Client TTFB: ${ttfb} ms | DOM Ready: ${domComplete} ms (W3C Navigation Timing)`);
          }
        }
      } catch (e) {
        // Fallback silently if performance API not supported
      }
    }, 500);
  });
});
