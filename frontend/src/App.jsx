import { useState } from "react";
import "./App.css";

const services = [
  {
    name: "Checkout Service",
    status: "Degraded",
    port: 8001,
    uptime: "99.91%",
    latency: "115ms",
    description: "Handles checkout requests and payment orchestration.",
  },
  {
    name: "Order Service",
    status: "Critical",
    port: 8002,
    uptime: "98.42%",
    latency: "236ms",
    description: "Processes orders and communicates with the order database.",
  },
  {
    name: "Payment Service",
    status: "Healthy",
    port: 8003,
    uptime: "99.98%",
    latency: "84ms",
    description: "Handles payment authorization and transaction processing.",
  },
  {
    name: "Inventory Service",
    status: "Healthy",
    port: 8004,
    uptime: "99.99%",
    latency: "42ms",
    description: "Manages product inventory and stock availability.",
  },
];

const deployments = [
  {
    service: "Checkout Service",
    version: "v1.8.2",
    commit: "a82f31c",
    time: "18 minutes ago",
    status: "Active",
  },
  {
    service: "Order Service",
    version: "v2.4.1",
    commit: "91be20a",
    time: "42 minutes ago",
    status: "Active",
  },
  {
    service: "Payment Service",
    version: "v3.1.0",
    commit: "8cf129d",
    time: "2 hours ago",
    status: "Active",
  },
  {
    service: "Inventory Service",
    version: "v2.9.4",
    commit: "bc832aa",
    time: "5 hours ago",
    status: "Active",
  },
];

const incidents = [
  {
    title: "Checkout requests failing",
    severity: "Critical",
    service: "Order Service",
    status: "Investigating",
    time: "12 minutes ago",
  },
  {
    title: "Elevated checkout latency",
    severity: "High",
    service: "Checkout Service",
    status: "Investigating",
    time: "24 minutes ago",
  },
  {
    title: "Order database timeout",
    severity: "Medium",
    service: "Order Service",
    status: "Resolved",
    time: "Yesterday",
  },
];

function StatusBadge({ status }) {
  return (
    <span className={`status-badge ${status.toLowerCase()}`}>
      <span className="status-dot" />
      {status}
    </span>
  );
}

function App() {
  const [page, setPage] = useState("home");
  const [activeTab, setActiveTab] = useState("overview");
  const [incident, setIncident] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function investigate() {
    if (!incident.trim()) return;

    setLoading(true);
    setResult("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/investigate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ incident }),
        }
      );

      if (!response.ok) {
        throw new Error("Investigation request failed");
      }

      const data = await response.json();
      setResult(data.analysis);
    } catch (error) {
      setResult(
        "Unable to connect to OpsPilot. Make sure the FastAPI backend is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  if (page === "home") {
    return (
      <div className="landing">
        <nav className="landing-nav">
          <div className="brand">
            <div className="brand-icon">O</div>
            <span>OpsPilot</span>
          </div>

          <button className="nav-button" onClick={() => setPage("dashboard")}>
            Open Dashboard →
          </button>
        </nav>

        <main className="hero">
          <div className="hero-badge">
            <span /> AI-powered incident intelligence
          </div>

          <h1>
            Understand production
            <br />
            <span>incidents faster.</span>
          </h1>

          <p className="hero-text">
            OpsPilot investigates production incidents using service health,
            logs, deployments, historical knowledge, and AI to help engineers
            identify the likely root cause faster.
          </p>

          <div className="hero-actions">
            <button
              className="primary-button"
              onClick={() => setPage("dashboard")}
            >
              Investigate an Incident
              <span>→</span>
            </button>

            <button
              className="secondary-button"
              onClick={() => setPage("dashboard")}
            >
              Explore Dashboard
            </button>
          </div>

          <div className="hero-preview">
            <div className="preview-top">
              <div>
                <small>OPS PILOT</small>
                <h3>Production Overview</h3>
              </div>
              <span className="live-pill">
                <i /> Live
              </span>
            </div>

            <div className="preview-grid">
              <div>
                <span>Services</span>
                <strong>4</strong>
                <small className="green">3 healthy</small>
              </div>

              <div>
                <span>Active Incidents</span>
                <strong>2</strong>
                <small className="red">1 critical</small>
              </div>

              <div>
                <span>Deployments</span>
                <strong>12</strong>
                <small>Last 24 hours</small>
              </div>

              <div>
                <span>System Health</span>
                <strong>96%</strong>
                <small className="green">Operational</small>
              </div>
            </div>
          </div>
        </main>

        <section className="feature-section">
          <div className="section-label">HOW IT WORKS</div>

          <h2>
            From alert to
            <br />
            <span>root cause.</span>
          </h2>

          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-number">01</div>
              <h3>Collect Evidence</h3>
              <p>
                OpsPilot gathers service health, logs, metrics and deployment
                information.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-number">02</div>
              <h3>Connect the Dots</h3>
              <p>
                Historical incidents and system dependencies provide additional
                context.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-number">03</div>
              <h3>Investigate</h3>
              <p>
                AI analyzes the evidence and produces a likely root cause with
                supporting evidence.
              </p>
            </div>
          </div>
        </section>

        <footer>
          <span>OpsPilot</span>
          <span>AI-powered production intelligence</span>
        </footer>
      </div>
    );
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand sidebar-brand">
          <div className="brand-icon">O</div>
          <span>OpsPilot</span>
        </div>

        <div className="sidebar-section">
          <span className="sidebar-label">MONITOR</span>

          <button
            className={activeTab === "overview" ? "side-link active" : "side-link"}
            onClick={() => setActiveTab("overview")}
          >
            <span>◈</span> Overview
          </button>

          <button
            className={activeTab === "services" ? "side-link active" : "side-link"}
            onClick={() => setActiveTab("services")}
          >
            <span>◇</span> Services
          </button>

          <button
            className={
              activeTab === "deployments" ? "side-link active" : "side-link"
            }
            onClick={() => setActiveTab("deployments")}
          >
            <span>↗</span> Deployments
          </button>

          <button
            className={
              activeTab === "incidents" ? "side-link active" : "side-link"
            }
            onClick={() => setActiveTab("incidents")}
          >
            <span>!</span> Incidents
            <b>3</b>
          </button>
        </div>

        <div className="sidebar-section">
          <span className="sidebar-label">INTELLIGENCE</span>

          <button
            className={
              activeTab === "investigate" ? "side-link active" : "side-link"
            }
            onClick={() => setActiveTab("investigate")}
          >
            <span>✦</span> AI Investigation
          </button>
        </div>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="system-dot" />
            <div>
              <strong>All systems</strong>
              <small>Operational</small>
            </div>
          </div>

          <button className="back-button" onClick={() => setPage("home")}>
            ← Back to intro
          </button>
        </div>
      </aside>

      <main className="dashboard">
        <header className="dashboard-header">
          <div>
            <div className="breadcrumb">OPSPILOT / MONITOR</div>
            <h1>
              {activeTab === "overview" && "Production Overview"}
              {activeTab === "services" && "Services"}
              {activeTab === "deployments" && "Deployments"}
              {activeTab === "incidents" && "Incidents"}
              {activeTab === "investigate" && "AI Investigation"}
            </h1>
          </div>

          <div className="header-actions">
            <span className="environment">
              <i /> Production
            </span>
            <button className="avatar">SR</button>
          </div>
        </header>

        {activeTab === "overview" && (
          <>
            <section className="stats">
              <div className="stat-card">
                <span>System Health</span>
                <strong>96%</strong>
                <small className="green">↑ 2.4% from yesterday</small>
              </div>

              <div className="stat-card">
                <span>Active Incidents</span>
                <strong>2</strong>
                <small className="red">1 requires attention</small>
              </div>

              <div className="stat-card">
                <span>Services</span>
                <strong>4</strong>
                <small className="green">3 healthy</small>
              </div>

              <div className="stat-card">
                <span>Deployments</span>
                <strong>12</strong>
                <small>Last 24 hours</small>
              </div>
            </section>

            <section className="content-grid">
              <div className="panel incident-panel">
                <div className="panel-header">
                  <div>
                    <span className="panel-eyebrow">ACTIVE INCIDENT</span>
                    <h2>Checkout requests failing</h2>
                  </div>
                  <StatusBadge status="Critical" />
                </div>

                <p>
                  Checkout requests are failing and the Order Service is
                  experiencing database timeouts.
                </p>

                <div className="incident-meta">
                  <span>Order Service</span>
                  <span>12 minutes ago</span>
                </div>

                <button
                  className="investigate-button"
                  onClick={() => setActiveTab("investigate")}
                >
                  ✦ Investigate with AI →
                </button>
              </div>

              <div className="panel">
                <div className="panel-header">
                  <div>
                    <span className="panel-eyebrow">SERVICES</span>
                    <h2>Service Health</h2>
                  </div>

                  <button
                    className="view-button"
                    onClick={() => setActiveTab("services")}
                  >
                    View all
                  </button>
                </div>

                <div className="service-list">
                  {services.map((service) => (
                    <div className="service-row" key={service.name}>
                      <div className="service-name">
                        <span
                          className={`health-dot ${service.status.toLowerCase()}`}
                        />
                        <div>
                          <strong>{service.name}</strong>
                          <small>:{service.port}</small>
                        </div>
                      </div>

                      <StatusBadge status={service.status} />
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="panel deployments-panel">
              <div className="panel-header">
                <div>
                  <span className="panel-eyebrow">RECENT ACTIVITY</span>
                  <h2>Latest Deployments</h2>
                </div>

                <button
                  className="view-button"
                  onClick={() => setActiveTab("deployments")}
                >
                  View all
                </button>
              </div>

              <div className="table">
                {deployments.map((deployment) => (
                  <div className="table-row" key={deployment.commit}>
                    <strong>{deployment.service}</strong>
                    <span>{deployment.version}</span>
                    <code>{deployment.commit}</code>
                    <span>{deployment.time}</span>
                    <StatusBadge status={deployment.status} />
                  </div>
                ))}
              </div>
            </section>
          </>
        )}

        {activeTab === "services" && (
          <section className="page-content">
            <div className="page-intro">
              <p>
                Monitor the health and performance of every service in your
                production environment.
              </p>
            </div>

            <div className="service-cards">
              {services.map((service) => (
                <div className="large-service-card" key={service.name}>
                  <div className="large-service-top">
                    <div className={`large-service-icon ${service.status.toLowerCase()}`}>
                      ◇
                    </div>
                    <StatusBadge status={service.status} />
                  </div>

                  <h2>{service.name}</h2>
                  <p>{service.description}</p>

                  <div className="service-metrics">
                    <div>
                      <span>Port</span>
                      <strong>{service.port}</strong>
                    </div>

                    <div>
                      <span>Uptime</span>
                      <strong>{service.uptime}</strong>
                    </div>

                    <div>
                      <span>Latency</span>
                      <strong>{service.latency}</strong>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === "deployments" && (
          <section className="page-content">
            <div className="page-intro">
              <p>
                Track application releases, versions and deployment history
                across your production services.
              </p>
            </div>

            <div className="panel">
              <div className="table deployment-table">
                <div className="table-header">
                  <span>Service</span>
                  <span>Version</span>
                  <span>Commit</span>
                  <span>Deployed</span>
                  <span>Status</span>
                </div>

                {deployments.map((deployment) => (
                  <div className="table-row" key={deployment.commit}>
                    <strong>{deployment.service}</strong>
                    <span>{deployment.version}</span>
                    <code>{deployment.commit}</code>
                    <span>{deployment.time}</span>
                    <StatusBadge status={deployment.status} />
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        {activeTab === "incidents" && (
          <section className="page-content">
            <div className="page-intro">
              <p>
                Investigate active production problems and review previously
                resolved incidents.
              </p>
            </div>

            <div className="incident-list">
              {incidents.map((item) => (
                <div className="incident-card" key={item.title}>
                  <div className="incident-card-icon">!</div>

                  <div className="incident-card-main">
                    <div className="incident-card-top">
                      <h2>{item.title}</h2>
                      <StatusBadge status={item.severity} />
                    </div>

                    <p>
                      {item.service} · {item.time}
                    </p>
                  </div>

                  <span className={`incident-status ${item.status.toLowerCase()}`}>
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {activeTab === "investigate" && (
          <section className="investigation-page">
            <div className="investigation-hero">
              <div className="ai-icon">✦</div>
              <span className="panel-eyebrow">AI INCIDENT INVESTIGATION</span>

              <h2>What happened?</h2>

              <p>
                Describe the production incident and OpsPilot will analyze
                available evidence, historical incidents and service data.
              </p>
            </div>

            <div className="investigation-box">
              <textarea
                value={incident}
                onChange={(e) => setIncident(e.target.value)}
                placeholder="Example: Checkout requests are failing and the Order Service is experiencing database timeouts."
              />

              <div className="investigation-bottom">
                <span>OpsPilot will collect production evidence automatically.</span>

                <button
                  className="primary-button"
                  onClick={investigate}
                  disabled={loading || !incident.trim()}
                >
                  {loading ? (
                    <>
                      <span className="spinner" />
                      Investigating...
                    </>
                  ) : (
                    <>✦ Investigate Incident →</>
                  )}
                </button>
              </div>
            </div>

            {result && (
              <div className="analysis-panel">
                <div className="analysis-header">
                  <div>
                    <span className="panel-eyebrow">INVESTIGATION COMPLETE</span>
                    <h2>AI Analysis</h2>
                  </div>

                  <span className="confidence">AI GENERATED</span>
                </div>

                <div className="analysis-content">
                  {result.split("\n").map((line, index) => {
                    if (!line.trim()) {
                      return <div className="analysis-space" key={index} />;
                    }

                    if (
                      line.includes("Incident Summary") ||
                      line.includes("Severity") ||
                      line.includes("Likely Root Cause") ||
                      line.includes("Evidence") ||
                      line.includes("Historical Context") ||
                      line.includes("Recent Deployment Analysis") ||
                      line.includes("Recommended Actions") ||
                      line.includes("Confidence")
                    ) {
                      return <h3 key={index}>{line.replace(/[#*-]/g, "").trim()}</h3>;
                    }

                    return <p key={index}>{line.replace(/\*\*/g, "").trim()}</p>;
                  })}
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
