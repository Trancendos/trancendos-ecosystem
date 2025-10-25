package com.trancendos.alervato.controller;

import com.trancendos.alervato.model.Cost;
import com.trancendos.alervato.service.CostService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/costs")
public class CostController {

    @Autowired
    private CostService costService;

    @GetMapping
    public List<Cost> getAllCosts() {
        return costService.findAll();
    }

    @PostMapping
    public Cost createCost(@RequestBody Cost cost) {
        return costService.save(cost);
    }

    @PostMapping("/{id}/approve")
    public ResponseEntity<Cost> approveCost(@PathVariable Long id) {
        try {
            Cost approvedCost = costService.approve(id);
            return ResponseEntity.ok(approvedCost);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping("/{id}/reject")
    public ResponseEntity<Cost> rejectCost(@PathVariable Long id) {
        try {
            Cost rejectedCost = costService.reject(id);
            return ResponseEntity.ok(rejectedCost);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
