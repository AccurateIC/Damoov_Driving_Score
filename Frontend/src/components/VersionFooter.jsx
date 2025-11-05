import React from "react";
import version from "../version.json";

export default function VersionFooter() {
  return (
    <footer style={{ textAlign: "center", fontSize: "12px", color: "#666" }}>
      Build #{version.buildNumber} | {version.branch}@{version.commit} | {version.buildDate}
    </footer>
  );
}
