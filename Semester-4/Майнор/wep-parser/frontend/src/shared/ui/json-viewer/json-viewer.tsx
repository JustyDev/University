import React from 'react';
import styles from './json-viewer.module.css';

interface JsonViewerProps {
  data: any;
}

export const JsonViewer: React.FC<JsonViewerProps> = ({ data }) => {
  return (
    <pre className={styles.container}>
      {JSON.stringify(data, null, 2)}
    </pre>
  );
};
