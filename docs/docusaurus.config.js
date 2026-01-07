// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Behaverse Schemas',
  tagline: 'Custom schemas for cognitive and behavioral sciences',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://behaverse.org',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/schemas/',

  // GitHub pages deployment config.
  organizationName: 'behaverse',
  projectName: 'schemas',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/behaverse/schemas/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      // image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Behaverse Schemas',
        // logo: {
        //   alt: 'Behaverse Logo',
        //   src: 'img/logo.svg',
        // },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'bcsvwSidebar',
            position: 'left',
            label: 'bcsvw',
          },
          {
            type: 'docSidebar',
            sidebarId: 'catalogSidebar',
            position: 'left',
            label: 'catalog',
          },
          {
            type: 'docSidebar',
            sidebarId: 'datasetSidebar',
            position: 'left',
            label: 'dataset',
          },
          {
            type: 'docSidebar',
            sidebarId: 'studyflowSidebar',
            position: 'left',
            label: 'studyflow',
          },
          {
            href: 'https://github.com/behaverse/schemas',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Schemas',
            items: [
              {
                label: 'bcsvw',
                to: '/bcsvw',
              },
              {
                label: 'catalog',
                to: '/catalog',
              },
              {
                label: 'dataset',
                to: '/dataset',
              },
              {
                label: 'studyflow',
                to: '/studyflow',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/behaverse/schemas',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Behaverse',
                href: 'https://behaverse.org',
              },
            ],
          },
        ],
        copyright: `Licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['json', 'yaml', 'python', 'bash'],
      },
      // Algolia search - uncomment and configure when credentials are available
      // algolia: {
      //   appId: 'YOUR_APP_ID',
      //   apiKey: 'YOUR_SEARCH_API_KEY',
      //   indexName: 'behaverse-schemas',
      //   contextualSearch: true,
      //   searchParameters: {},
      //   searchPagePath: 'search',
      // },
    }),
};

export default config;
