package com.trancendos.alervato.controller;

import com.trancendos.alervato.model.CustomerService;
import com.trancendos.alervato.service.OfferedService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/customer-services")
public class CustomerServiceController {

    @Autowired
    private OfferedService offeredService;

    @GetMapping
    public List<CustomerService> getAllCustomerServices() {
        return offeredService.findAll();
    }

    @PostMapping
    public CustomerService createCustomerService(@RequestBody CustomerService customerService) {
        return offeredService.save(customerService);
    }
}
