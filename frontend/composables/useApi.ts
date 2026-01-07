import type { IlceResponse, EczaneResponse } from "~/types";

export const useApi = () => {
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBase;

  /**
   * Fetch Istanbul districts (il_id = 1)
   */
  const fetchIstanbulDistricts = () => {
    return useFetch<IlceResponse[]>(`${baseURL}/iller/1/ilceler`, {
      key: "istanbul-districts",
    });
  };

  /**
   * Fetch all pharmacies
   */
  const fetchEczaneler = () => {
    return useFetch<EczaneResponse[]>(`${baseURL}/eczaneler/`, {
      key: "eczaneler",
    });
  };

  return {
    fetchIstanbulDistricts,
    fetchEczaneler,
  };
};
