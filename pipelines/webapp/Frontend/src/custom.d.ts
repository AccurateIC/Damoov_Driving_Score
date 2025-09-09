interface ProcessEnv {
  readonly REACT_APP_BASE_URL: string;
}

declare var process: {
  env: ProcessEnv;
};
