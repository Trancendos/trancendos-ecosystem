package com.trancendos.alervato.service;

import com.trancendos.alervato.model.Cost;
import com.trancendos.alervato.model.CostStatus;
import com.trancendos.alervato.repository.CostRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CostService {

    @Autowired
    private CostRepository costRepository;

    public List<Cost> findAll() {
        return costRepository.findAll();
    }

    public Cost save(Cost cost) {
        return costRepository.save(cost);
    }

    public Optional<Cost> findById(Long id) {
        return costRepository.findById(id);
    }

    public Cost approve(Long id) {
        Cost cost = costRepository.findById(id).orElseThrow(() -> new RuntimeException("Cost not found"));
        cost.setStatus(CostStatus.APPROVED);
        return costRepository.save(cost);
    }

    public Cost reject(Long id) {
        Cost cost = costRepository.findById(id).orElseThrow(() -> new RuntimeException("Cost not found"));
        cost.setStatus(CostStatus.REJECTED);
        return costRepository.save(cost);
    }
}
