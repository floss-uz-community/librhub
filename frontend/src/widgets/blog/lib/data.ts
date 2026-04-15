export interface BlogPost {
  id: number;
  title: string;
  content: string;
  author: {
    name: string;
    avatar: string;
    role: string;
  };
  tags: string[];
  stats: {
    views: number;
    comments: number;
    likes: number;
    dislikes: number;
  };
  publishedAt: string;
  readTime: string;
  isSaved: boolean;
}

export interface MostReadPost {
  id: number;
  title: string;
  author: string;
  views: number;
  readTime: string;
}

export interface TopChannel {
  id: number;
  name: string;
  avatar: string;
  subscribers: number;
  posts: number;
}

export const blogPosts: BlogPost[] = [
  {
    id: 1,
    title: "Getting Started with Next.js 14 and App Router",
    content: "Learn how to build modern web applications with Next.js 14's new App Router and its powerful features. This comprehensive guide covers everything from basic setup to advanced patterns...",
    author: {
      name: "John Doe",
      avatar: "/images/avatar1.jpg",
      role: "Senior Developer"
    },
    tags: ["Next.js", "React", "Web Development"],
    stats: {
      views: 1250,
      comments: 23,
      likes: 45,
      dislikes: 2
    },
    publishedAt: "2024-01-15",
    readTime: "5 min read",
    isSaved: false
  },
  {
    id: 2,
    title: "Mastering TypeScript: Advanced Patterns and Best Practices",
    content: "Dive deep into TypeScript's advanced features and learn how to write more maintainable and type-safe code. We'll explore generics, utility types, and advanced patterns...",
    author: {
      name: "Jane Smith",
      avatar: "/images/avatar2.jpg",
      role: "TypeScript Expert"
    },
    tags: ["TypeScript", "Programming", "Best Practices"],
    stats: {
      views: 2100,
      comments: 67,
      likes: 89,
      dislikes: 5
    },
    publishedAt: "2024-01-12",
    readTime: "8 min read",
    isSaved: true
  },
  {
    id: 3,
    title: "Building Scalable React Applications with Modern Architecture",
    content: "Explore modern patterns for building large-scale React applications that are maintainable and performant. Learn about state management, component architecture, and performance optimization...",
    author: {
      name: "Mike Johnson",
      avatar: "/images/avatar3.jpg",
      role: "Frontend Architect"
    },
    tags: ["React", "Architecture", "Scalability"],
    stats: {
      views: 1800,
      comments: 34,
      likes: 72,
      dislikes: 3
    },
    publishedAt: "2024-01-10",
    readTime: "12 min read",
    isSaved: false
  },
  {
    id: 4,
    title: "CSS Grid vs Flexbox: When to Use What",
    content: "A comprehensive comparison of CSS Grid and Flexbox, including practical examples and use cases. Learn when to use each layout method for optimal results...",
    author: {
      name: "Sarah Wilson",
      avatar: "/images/avatar4.jpg",
      role: "CSS Expert"
    },
    tags: ["CSS", "Layout", "Web Design"],
    stats: {
      views: 3200,
      comments: 89,
      likes: 156,
      dislikes: 8
    },
    publishedAt: "2024-01-08",
    readTime: "6 min read",
    isSaved: true
  },
  {
    id: 5,
    title: "Node.js Performance Optimization Tips",
    content: "Discover proven techniques to optimize your Node.js applications for better performance. From memory management to async patterns, we cover it all...",
    author: {
      name: "Alex Thompson",
      avatar: "/images/avatar5.jpg",
      role: "Backend Engineer"
    },
    tags: ["Node.js", "Performance", "Backend"],
    stats: {
      views: 2800,
      comments: 45,
      likes: 98,
      dislikes: 4
    },
    publishedAt: "2024-01-05",
    readTime: "10 min read",
    isSaved: false
  }
];

export const mostReadPosts: MostReadPost[] = [
  {
    id: 1,
    title: "Complete Guide to React Hooks",
    author: "Sarah Wilson",
    views: 15420,
    readTime: "6 min"
  },
  {
    id: 2,
    title: "Understanding JavaScript Closures",
    author: "David Chen",
    views: 12300,
    readTime: "4 min"
  },
  {
    id: 3,
    title: "CSS Grid vs Flexbox: When to Use What",
    author: "Emily Rodriguez",
    views: 9800,
    readTime: "7 min"
  },
  {
    id: 4,
    title: "Node.js Performance Optimization Tips",
    author: "Alex Thompson",
    views: 8700,
    readTime: "9 min"
  },
  {
    id: 5,
    title: "Building RESTful APIs with Express",
    author: "Maria Garcia",
    views: 7500,
    readTime: "8 min"
  }
];

export const topChannels: TopChannel[] = [
  {
    id: 1,
    name: "Web Dev Weekly",
    avatar: "/images/channel1.jpg",
    subscribers: 125000,
    posts: 45
  },
  {
    id: 2,
    name: "React Masters",
    avatar: "/images/channel2.jpg",
    subscribers: 98000,
    posts: 32
  },
  {
    id: 3,
    name: "JavaScript Daily",
    avatar: "/images/channel3.jpg",
    subscribers: 156000,
    posts: 67
  },
  {
    id: 4,
    name: "CSS Tricks Pro",
    avatar: "/images/channel4.jpg",
    subscribers: 89000,
    posts: 28
  },
  {
    id: 5,
    name: "Full Stack Dev",
    avatar: "/images/channel5.jpg",
    subscribers: 112000,
    posts: 41
  }
];

export const topics = [
  'Technology',
  'Programming',
  'Web Development',
  'Mobile Development',
  'Data Science',
  'Artificial Intelligence',
  'DevOps',
  'Design',
  'Productivity',
  'Career'
];

export const categories = [
  { name: 'Tutorials', count: 24 },
  { name: 'News', count: 18 },
  { name: 'Reviews', count: 12 },
  { name: 'Opinions', count: 8 },
  { name: 'Guides', count: 15 },
  { name: 'Tools', count: 6 }
];
