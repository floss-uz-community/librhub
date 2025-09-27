import React from 'react';
import { blogPosts } from '../lib/data';
import { BlogPost } from './BlogPost';
import { Separator } from '@/shared/ui/separator';

export function BlogPostList() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className='flex items-center'>
          <h1 className="text-3xl font-bold">Latest Posts</h1>
          <Separator orientation="vertical" />
          <h1 className="text-3xl font-bold">Latest Posts</h1>
        </div>
        <div className="flex gap-2">
          <select className="px-3 py-2 border border-input bg-background rounded-md text-sm">
            <option value="latest">Latest</option>
            <option value="popular">Most Popular</option>
            <option value="trending">Trending</option>
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
