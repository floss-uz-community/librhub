import React from 'react';
import { LeftSidebar } from '@/widgets/blog/ui/LeftSidebar';
import { BlogPostList } from '@/widgets/blog/ui/BlogPostList';
import { RightSidebar } from '@/widgets/blog/ui/RightSidebar';

export function BlogLayout() {
  return (
    <div className="min-h-screen bg-background">
      {/* Main Content */}
      <div className="my-container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">        
          {/* Main Content - Blog Posts */}
          <main className="lg:col-span-9 order-1 lg:order-2">
            <BlogPostList />
          </main>

          {/* Right Sidebar - Most Read and Top Channels */}
          <aside className="lg:col-span-3 order-3">
            <div className="sticky top-4">
              <RightSidebar />
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
