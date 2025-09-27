import { ENDP_POSTS } from '@/shared/constants/apiEndpoints';
import { ReqWithPagination } from './types';
import { AxiosResponse } from 'axios';
import { TestApiType } from '@/shared/types/testApi';
import httpClient from './httpClient';

const getPosts = async (
  pagination?: ReqWithPagination,
): Promise<AxiosResponse<TestApiType>> => {
  const response = await httpClient.get(ENDP_POSTS, { params: pagination });
  return response;
};

export { getPosts };
