"use client"
import { Button } from '@/shared/ui/button';
import { useState } from 'react';
import { blogPosts } from '../lib/data';
import { BlogPost } from './BlogPost';

type TabType = 'relevant' | 'latest' | 'top';

export function BlogPostList() {
  const [activeTab, setActiveTab] = useState<TabType>('latest');

  const tabs = [
    { id: 'relevant' as TabType, label: 'Relevant' },
    { id: 'latest' as TabType, label: 'Latest' },
    { id: 'top' as TabType, label: 'Top' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
         {/* Tabs */}
         <div className="flex space-x-1 bg-muted p-1 rounded-lg w-fit">
          {tabs.map((tab) => (
            <Button
              key={tab.id}
              variant={activeTab === tab.id ? "default" : "ghost"}
              size="sm"
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 text-sm font-medium transition-colors ${activeTab === tab.id
                ? 'text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
                }`}
            >
              {tab.label}
            </Button>
          ))}
        </div>

        <div className="flex gap-2">
          <select className="px-3 py-2 border border-input bg-background rounded-md text-sm">
            <option value="all">All Categories</option>
            <option value="tutorials">Tutorials</option>
            <option value="news">News</option>
            <option value="reviews">Reviews</option>
          </select>
        </div>
      </div>



      <div className="space-y-6">
        {blogPosts.map((post) => (
          <BlogPost key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}
