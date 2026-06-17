module.exports = {
  darkMode: 'class',
  content: ['./index.html', './work.html'],
  theme: { extend: {
    colors: {
      bg: 'rgb(var(--bg) / <alpha-value>)', surface: 'rgb(var(--surface) / <alpha-value>)',
      ink: 'rgb(var(--ink) / <alpha-value>)', muted: 'rgb(var(--muted) / <alpha-value>)',
      line: 'rgb(var(--line) / <alpha-value>)', accent: 'rgb(var(--accent) / <alpha-value>)',
      'accent-hover': 'rgb(var(--accent-hover) / <alpha-value>)',
    },
    fontFamily: {
      mono: ['"JetBrains Mono"','ui-monospace','SFMono-Regular','Menlo','"PingFang TC"','"Microsoft JhengHei"','"Noto Sans TC"','monospace'],
      sans: ['"JetBrains Mono"','ui-monospace','SFMono-Regular','Menlo','"PingFang TC"','"Microsoft JhengHei"','"Noto Sans TC"','monospace'],
      serif: ['"Taipei Sans TC"','"PingFang TC"','"Noto Sans TC"','sans-serif'],
      tp: ['"Taipei Sans TC"','"PingFang TC"','"Noto Sans TC"','sans-serif'],
    },
    maxWidth: { content: '1200px', prose: '760px' },
  }},
};
