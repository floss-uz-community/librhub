import { getPosts } from '@/shared/config/api/testApi';

export default async function Home() {
  const res = await getPosts({ _limit: 1 });
  console.log('SSR res', res.data);

  return (
    <div className='my-container'>
      salom
    </div>
  );
}
